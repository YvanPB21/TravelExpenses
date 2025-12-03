"""Implementación de almacenamiento en Firebase Firestore para Split Bill."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from functools import lru_cache
import time

from google.cloud.firestore_v1.base_query import FieldFilter

from db.firebase_client import FirebaseConfig, get_firestore_client
from db.config import ENABLE_CACHE, CACHE_TTL_SECONDS, BATCH_SIZE, DEBUG_FIRESTORE
from models import Item, Person, SharedCost, Trip


class PersistenceError(RuntimeError):
    """Error base de persistencia."""


class NotFoundError(PersistenceError):
    """Se lanzó cuando una entidad no existe."""


class FirestoreStore:
    """Capa de acceso a Firestore para los recursos del viaje."""

    def __init__(self, config: FirebaseConfig | None = None):
        self._config = config or FirebaseConfig()
        self._db = get_firestore_client(self._config)

        # Referencias a colecciones
        self._trips = self._db.collection('trips')
        self._persons = self._db.collection('persons')
        self._items = self._db.collection('items')
        self._shared_costs = self._db.collection('shared_costs')
        self._metadata = self._db.collection('metadata')

        # Caché en memoria para reducir lecturas repetidas
        self._cache = {
            'trips': {},
            'persons': {},
            'items': {},
            'shared_costs': {},
            'last_clear': time.time()
        }
        self._cache_ttl = CACHE_TTL_SECONDS
        self._enable_cache = ENABLE_CACHE

        if DEBUG_FIRESTORE:
            print(f"🔥 Firestore Store inicializado (cache: {self._enable_cache}, TTL: {self._cache_ttl}s)")

    # Cache helpers -----------------------------------------------------------
    def _clear_cache_if_needed(self):
        """Limpia el caché si ha expirado el TTL."""
        if time.time() - self._cache['last_clear'] > self._cache_ttl:
            self._cache = {
                'trips': {},
                'persons': {},
                'items': {},
                'shared_costs': {},
                'last_clear': time.time()
            }

    def _invalidate_cache(self, cache_type: str, key: str = None):
        """Invalida una entrada específica o todo el tipo de caché."""
        if key:
            self._cache.get(cache_type, {}).pop(key, None)
        else:
            self._cache[cache_type] = {}

    def _get_cached(self, cache_type: str, key: str, fetch_func):
        """Obtiene del caché o ejecuta fetch_func si no existe/expiró."""
        if not self._enable_cache:
            if DEBUG_FIRESTORE:
                print(f"📖 Firestore READ (no cache): {cache_type}/{key}")
            return fetch_func()

        self._clear_cache_if_needed()

        if key in self._cache.get(cache_type, {}):
            if DEBUG_FIRESTORE:
                print(f"⚡ Cache HIT: {cache_type}/{key}")
            return self._cache[cache_type][key]

        if DEBUG_FIRESTORE:
            print(f"📖 Firestore READ (cache miss): {cache_type}/{key}")
        result = fetch_func()
        if result is not None:
            self._cache[cache_type][key] = result
        return result

    # Trips -------------------------------------------------------------------
    def list_trips(self) -> List[Trip]:
        """Lista todos los viajes."""
        docs = self._trips.stream()
        return [self._doc_to_trip(doc) for doc in docs]

    def get_trip(self, trip_id: int) -> Optional[Trip]:
        """Obtiene un viaje por ID."""
        doc = self._trips.document(str(trip_id)).get()
        if not doc.exists:
            return None
        return self._doc_to_trip(doc)

    def add_trip(self, name: str, description: str = "", days: int = 1) -> Trip:
        """Agrega un nuevo viaje."""
        trip_id = self._get_next_id('trip')
        trip = Trip(
            id=trip_id,
            name=name,
            description=description,
            days=days,
            created_at=datetime.now()
        )

        trip_data = {
            'id': trip.id,
            'name': trip.name,
            'description': trip.description,
            'days': trip.days,
            'created_at': trip.created_at.isoformat()
        }

        self._trips.document(str(trip_id)).set(trip_data)
        self._init_trip_counters(trip_id)
        return trip

    def remove_trip(self, trip_id: int) -> bool:
        """Elimina un viaje y todos sus datos asociados."""
        batch = self._db.batch()
        batch_count = 0

        # Eliminar viaje
        batch.delete(self._trips.document(str(trip_id)))
        batch_count += 1

        # Eliminar personas del viaje
        persons = self._persons.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        for person in persons:
            batch.delete(person.reference)
            batch_count += 1
            if batch_count >= 500:
                batch.commit()
                batch = self._db.batch()
                batch_count = 0

        # Eliminar items del viaje
        items = self._items.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        for item in items:
            batch.delete(item.reference)
            batch_count += 1
            if batch_count >= 500:
                batch.commit()
                batch = self._db.batch()
                batch_count = 0

        # Eliminar costos compartidos del viaje
        shared = self._shared_costs.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        for sc in shared:
            batch.delete(sc.reference)
            batch_count += 1
            if batch_count >= 500:
                batch.commit()
                batch = self._db.batch()
                batch_count = 0

        # Eliminar contadores del viaje
        batch.delete(self._metadata.document(f'counters_trip_{trip_id}'))
        batch_count += 1

        # Commit remaining operations
        if batch_count > 0:
            batch.commit()

        # Si es el viaje actual, limpiar
        current = self._get_current_trip_id()
        if current == trip_id:
            self._set_current_trip_id(None)

        # Invalidar caché
        self._invalidate_cache('trips', str(trip_id))
        self._invalidate_cache('persons', f'trip_{trip_id}')
        self._invalidate_cache('items', f'trip_{trip_id}')
        self._invalidate_cache('shared_costs', f'trip_{trip_id}')

        return True

    def set_current_trip(self, trip_id: int) -> bool:
        """Establece el viaje actual."""
        trip = self.get_trip(trip_id)
        if trip:
            self._set_current_trip_id(trip_id)
            return True
        return False

    def get_current_trip_id(self) -> Optional[int]:
        """Obtiene el ID del viaje actual."""
        return self._get_current_trip_id()

    # Persons -----------------------------------------------------------------
    def list_persons(self, trip_id: int) -> List[Person]:
        """Lista todas las personas de un viaje."""
        cache_key = f'trip_{trip_id}'

        def fetch():
            docs = self._persons.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
            return [self._doc_to_person(doc) for doc in docs]

        return self._get_cached('persons', cache_key, fetch)

    def get_person(self, trip_id: int, person_id: int) -> Optional[Person]:
        """Obtiene una persona por ID."""
        doc = self._persons.document(f'{trip_id}_{person_id}').get()
        if not doc.exists:
            return None
        return self._doc_to_person(doc)

    def add_person(self, trip_id: int, name: str) -> Person:
        """Agrega una persona a un viaje."""
        person_id = self._get_next_id('person', trip_id)
        person = Person(id=person_id, name=name)

        person_data = {
            'trip_id': trip_id,
            'id': person.id,
            'name': person.name
        }

        self._persons.document(f'{trip_id}_{person_id}').set(person_data)
        self._invalidate_cache('persons', f'trip_{trip_id}')
        return person

    def remove_person(self, trip_id: int, person_id: int) -> bool:
        """Elimina una persona de un viaje."""
        self._persons.document(f'{trip_id}_{person_id}').delete()

        # Remover de todos los items
        items = self._items.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        batch = self._db.batch()
        batch_count = 0

        for item_doc in items:
            item_data = item_doc.to_dict()
            person_ids = item_data.get('person_ids', [])
            if person_id in person_ids:
                person_ids.remove(person_id)
                batch.update(item_doc.reference, {'person_ids': person_ids})
                batch_count += 1

                # Firestore batch limit es 500 operaciones
                if batch_count >= 500:
                    batch.commit()
                    batch = self._db.batch()
                    batch_count = 0

        if batch_count > 0:
            batch.commit()

        self._invalidate_cache('persons', f'trip_{trip_id}')
        self._invalidate_cache('items', f'trip_{trip_id}')
        return True

    # Items -------------------------------------------------------------------
    def list_items(self, trip_id: int) -> List[Item]:
        """Lista todos los items de un viaje."""
        cache_key = f'trip_{trip_id}'

        def fetch():
            docs = self._items.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
            return [self._doc_to_item(doc) for doc in docs]

        return self._get_cached('items', cache_key, fetch)

    def get_item(self, trip_id: int, item_id: int) -> Optional[Item]:
        """Obtiene un item por ID."""
        doc = self._items.document(f'{trip_id}_{item_id}').get()
        if not doc.exists:
            return None
        return self._doc_to_item(doc)

    def add_item(self, trip_id: int, name: str, quantity: int, unit_price: float,
                 day: int = 1, url: str = "", paid_by_person_id: int = None) -> Item:
        """Agrega un item a un viaje."""
        item_id = self._get_next_id('item', trip_id)
        item = Item(
            id=item_id,
            name=name,
            quantity=quantity,
            unit_price=unit_price,
            day=day,
            url=url,
            paid_by_person_id=paid_by_person_id
        )

        item_data = {
            'trip_id': trip_id,
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'day': item.day,
            'url': item.url,
            'person_ids': [],
            'paid_by_person_id': item.paid_by_person_id
        }

        self._items.document(f'{trip_id}_{item_id}').set(item_data)
        self._invalidate_cache('items', f'trip_{trip_id}')
        return item

    def update_item(self, trip_id: int, item_id: int, **fields) -> bool:
        """Actualiza un item."""
        doc_ref = self._items.document(f'{trip_id}_{item_id}')
        if not doc_ref.get().exists:
            return False

        update_data = {}
        if 'name' in fields and fields['name'] is not None:
            update_data['name'] = fields['name']
        if 'quantity' in fields and fields['quantity'] is not None:
            update_data['quantity'] = fields['quantity']
        if 'unit_price' in fields and fields['unit_price'] is not None:
            update_data['unit_price'] = fields['unit_price']
        if 'day' in fields and fields['day'] is not None:
            update_data['day'] = fields['day']
        if 'url' in fields and fields['url'] is not None:
            update_data['url'] = fields['url']
        if 'paid_by_person_id' in fields and fields['paid_by_person_id'] is not None:
            update_data['paid_by_person_id'] = fields['paid_by_person_id']

        if update_data:
            doc_ref.update(update_data)
            self._invalidate_cache('items', f'trip_{trip_id}')
        return True

    def remove_item(self, trip_id: int, item_id: int) -> bool:
        """Elimina un item."""
        self._items.document(f'{trip_id}_{item_id}').delete()
        self._invalidate_cache('items', f'trip_{trip_id}')
        return True

    def toggle_person_for_item(self, trip_id: int, item_id: int, person_id: int) -> bool:
        """Alterna la participación de una persona en un item."""
        doc_ref = self._items.document(f'{trip_id}_{item_id}')
        doc = doc_ref.get()

        if not doc.exists:
            return False

        data = doc.to_dict()
        person_ids = data.get('person_ids', [])

        if person_id in person_ids:
            person_ids.remove(person_id)
        else:
            person_ids.append(person_id)

        doc_ref.update({'person_ids': person_ids})
        self._invalidate_cache('items', f'trip_{trip_id}')
        return True

    def get_items_by_day(self, trip_id: int, day: int) -> List[Item]:
        """Obtiene items de un día específico."""
        # Usa caché de list_items y filtra en memoria (más rápido)
        all_items = self.list_items(trip_id)
        return [item for item in all_items if item.day == day]

    # Shared Costs ------------------------------------------------------------
    def list_shared_costs(self, trip_id: int) -> List[SharedCost]:
        """Lista todos los costos compartidos de un viaje."""
        cache_key = f'trip_{trip_id}'

        def fetch():
            docs = self._shared_costs.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
            return [self._doc_to_shared_cost(doc) for doc in docs]

        return self._get_cached('shared_costs', cache_key, fetch)

    def get_shared_cost(self, trip_id: int, shared_cost_id: int) -> Optional[SharedCost]:
        """Obtiene un costo compartido por ID."""
        doc = self._shared_costs.document(f'{trip_id}_{shared_cost_id}').get()
        if not doc.exists:
            return None
        return self._doc_to_shared_cost(doc)

    def add_shared_cost(self, trip_id: int, name: str, cost: float, day: int = 1, paid_by_person_ids: List[int] = None) -> SharedCost:
        """Agrega un costo compartido a un viaje."""
        shared_cost_id = self._get_next_id('shared_cost', trip_id)
        shared_cost = SharedCost(
            id=shared_cost_id,
            name=name,
            cost=cost,
            day=day,
            paid_by_person_ids=set(paid_by_person_ids or [])
        )

        shared_data = {
            'trip_id': trip_id,
            'id': shared_cost.id,
            'name': shared_cost.name,
            'cost': shared_cost.cost,
            'day': shared_cost.day,
            'paid_by_person_ids': paid_by_person_ids or []
        }

        self._shared_costs.document(f'{trip_id}_{shared_cost_id}').set(shared_data)
        self._invalidate_cache('shared_costs', f'trip_{trip_id}')
        return shared_cost

    def update_shared_cost(self, trip_id: int, shared_cost_id: int, **fields) -> bool:
        """Actualiza un costo compartido."""
        doc_ref = self._shared_costs.document(f'{trip_id}_{shared_cost_id}')
        if not doc_ref.get().exists:
            return False

        update_data = {}
        if 'name' in fields and fields['name'] is not None:
            update_data['name'] = fields['name']
        if 'cost' in fields and fields['cost'] is not None:
            update_data['cost'] = fields['cost']
        if 'day' in fields and fields['day'] is not None:
            update_data['day'] = fields['day']
        if 'paid_by_person_ids' in fields and fields['paid_by_person_ids'] is not None:
            update_data['paid_by_person_ids'] = fields['paid_by_person_ids']

        if update_data:
            doc_ref.update(update_data)
            self._invalidate_cache('shared_costs', f'trip_{trip_id}')
        return True

    def remove_shared_cost(self, trip_id: int, shared_cost_id: int) -> bool:
        """Elimina un costo compartido."""
        self._shared_costs.document(f'{trip_id}_{shared_cost_id}').delete()
        self._invalidate_cache('shared_costs', f'trip_{trip_id}')
        return True

    def get_shared_costs_by_day(self, trip_id: int, day: int) -> List[SharedCost]:
        """Obtiene costos compartidos de un día específico."""
        # Usa caché de list_shared_costs y filtra en memoria (más rápido)
        all_shared = self.list_shared_costs(trip_id)
        return [sc for sc in all_shared if sc.day == day]

    def clear_trip_data(self, trip_id: int):
        """Limpia todos los datos de un viaje (personas, items, shared costs)."""
        batch = self._db.batch()
        batch_count = 0

        # Eliminar personas
        persons = self._persons.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        for person in persons:
            batch.delete(person.reference)
            batch_count += 1
            if batch_count >= 500:
                batch.commit()
                batch = self._db.batch()
                batch_count = 0

        # Eliminar items
        items = self._items.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        for item in items:
            batch.delete(item.reference)
            batch_count += 1
            if batch_count >= 500:
                batch.commit()
                batch = self._db.batch()
                batch_count = 0

        # Eliminar costos compartidos
        shared = self._shared_costs.where(filter=FieldFilter('trip_id', '==', trip_id)).stream()
        for sc in shared:
            batch.delete(sc.reference)
            batch_count += 1
            if batch_count >= 500:
                batch.commit()
                batch = self._db.batch()
                batch_count = 0

        # Commit remaining operations
        if batch_count > 0:
            batch.commit()

        # Reiniciar contadores
        self._init_trip_counters(trip_id)

        # Invalidar caché
        self._invalidate_cache('persons', f'trip_{trip_id}')
        self._invalidate_cache('items', f'trip_{trip_id}')
        self._invalidate_cache('shared_costs', f'trip_{trip_id}')

    # Helpers -----------------------------------------------------------------
    def _get_next_id(self, counter_type: str, trip_id: int = None) -> int:
        """Obtiene el siguiente ID para un tipo de entidad."""
        if counter_type == 'trip':
            doc_ref = self._metadata.document('global_counters')
        else:
            doc_ref = self._metadata.document(f'counters_trip_{trip_id}')

        # Transacción para incrementar contador
        from google.cloud import firestore

        @firestore.transactional
        def update_counter(transaction, doc_ref, field):
            snapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                # Inicializar contadores
                transaction.set(doc_ref, {field: 2})
                return 1

            current = snapshot.get(field) if snapshot.get(field) else 1
            transaction.update(doc_ref, {field: current + 1})
            return current

        transaction = self._db.transaction()
        field_name = f'next_{counter_type}_id'
        return update_counter(transaction, doc_ref, field_name)

    def _init_trip_counters(self, trip_id: int):
        """Inicializa los contadores para un viaje."""
        doc_ref = self._metadata.document(f'counters_trip_{trip_id}')
        doc_ref.set({
            'next_person_id': 1,
            'next_item_id': 1,
            'next_shared_cost_id': 1
        })

    def _set_current_trip_id(self, trip_id: Optional[int]):
        """Establece el ID del viaje actual."""
        doc_ref = self._metadata.document('current_trip')
        if trip_id is None:
            doc_ref.delete()
        else:
            doc_ref.set({'trip_id': trip_id})

    def _get_current_trip_id(self) -> Optional[int]:
        """Obtiene el ID del viaje actual."""
        doc = self._metadata.document('current_trip').get()
        if doc.exists:
            return doc.to_dict().get('trip_id')
        return None

    # Deserializers -----------------------------------------------------------
    def _doc_to_trip(self, doc) -> Trip:
        """Convierte documento Firestore a Trip."""
        data = doc.to_dict()
        return Trip(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            days=data.get('days', 1),
            created_at=datetime.fromisoformat(data['created_at'])
        )

    def _doc_to_person(self, doc) -> Person:
        """Convierte documento Firestore a Person."""
        data = doc.to_dict()
        return Person(
            id=data['id'],
            name=data['name']
        )

    def _doc_to_item(self, doc) -> Item:
        """Convierte documento Firestore a Item."""
        data = doc.to_dict()
        return Item(
            id=data['id'],
            name=data['name'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            day=data.get('day', 1),
            url=data.get('url', ''),
            person_ids=set(data.get('person_ids', [])),
            paid_by_person_id=data.get('paid_by_person_id')
        )

    def _doc_to_shared_cost(self, doc) -> SharedCost:
        """Convierte documento Firestore a SharedCost."""
        data = doc.to_dict()
        return SharedCost(
            id=data['id'],
            name=data['name'],
            cost=data['cost'],
            day=data.get('day', 1),
            paid_by_person_ids=set(data.get('paid_by_person_ids', []))
        )


