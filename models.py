"""
Modelos de datos para la aplicación de división de gastos
"""
from typing import List, Set, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import os


@dataclass
class Trip:
    """Representa un viaje o evento de gastos compartidos"""
    id: int
    name: str
    description: str = ""
    days: int = 1  # Número de días del viaje
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Person:
    """Representa una persona en el grupo"""
    id: int
    name: str


@dataclass
class Item:
    """Representa un ítem de compra individual"""
    id: int
    name: str
    quantity: int  # Cantidad de unidades
    unit_price: float  # Precio por unidad
    day: int = 1  # Día del viaje al que pertenece este ítem
    url: str = ""  # URL del producto (opcional)
    person_ids: Set[int] = field(default_factory=set)  # IDs de personas que participan
    paid_by_person_id: int = None  # ID de la persona que pagó este ítem

    @property
    def total_cost(self) -> float:
        """Calcula el costo total (cantidad × precio unitario)"""
        return self.quantity * self.unit_price


@dataclass
class SharedCost:
    """Representa un costo compartido por todos"""
    id: int
    name: str
    cost: float
    day: int = 1  # Día del viaje al que pertenece este costo


class DataStore:
    """Almacena todos los datos en Firestore, organizados por viajes"""

    DATA_FILE = 'split_bill_data.json'  # Mantenido para compatibilidad

    def __init__(self, use_firestore: bool = True, firebase_config=None):
        self.use_firestore = use_firestore
        self.current_trip_id: Optional[int] = None

        if use_firestore:
            # Usar Firestore
            from db.firestore_store import FirestoreStore
            self._store = FirestoreStore(firebase_config)
            # Cargar current_trip_id desde Firestore
            self.current_trip_id = self._store.get_current_trip_id()
        else:
            # Modo legacy con JSON
            self.trips: List[Trip] = []
            self.trip_data: Dict[int, Dict] = {}
            self._next_trip_id = 1
            self._next_person_id = {}
            self._next_item_id = {}
            self._next_shared_cost_id = {}
            self.load_from_file()

    def save_to_file(self):
        """Guarda todos los datos en un archivo JSON (solo modo legacy)"""
        if self.use_firestore:
            # En modo Firestore, los datos ya están persistidos
            return

        try:
            data = {
                'trips': [self._trip_to_dict(trip) for trip in self.trips],
                'current_trip_id': self.current_trip_id,
                'trip_data': {},
                '_next_trip_id': self._next_trip_id,
                '_next_person_id': self._next_person_id,
                '_next_item_id': self._next_item_id,
                '_next_shared_cost_id': self._next_shared_cost_id
            }

            # Serializar trip_data
            for trip_id, trip_content in self.trip_data.items():
                data['trip_data'][str(trip_id)] = {
                    'persons': [self._person_to_dict(p) for p in trip_content['persons']],
                    'items': [self._item_to_dict(i) for i in trip_content['items']],
                    'shared_costs': [self._shared_cost_to_dict(sc) for sc in trip_content['shared_costs']]
                }

            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✓ Datos guardados en {self.DATA_FILE}")
        except Exception as e:
            print(f"✗ Error al guardar datos: {e}")

    def load_from_file(self):
        """Carga todos los datos desde un archivo JSON (solo modo legacy)"""
        if self.use_firestore:
            return

        if not os.path.exists(self.DATA_FILE):
            print(f"No existe archivo de datos. Iniciando con datos vacíos.")
            return

        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Cargar trips
            self.trips = [self._dict_to_trip(t) for t in data.get('trips', [])]
            self.current_trip_id = data.get('current_trip_id')
            self._next_trip_id = data.get('_next_trip_id', 1)
            self._next_person_id = data.get('_next_person_id', {})
            self._next_item_id = data.get('_next_item_id', {})
            self._next_shared_cost_id = data.get('_next_shared_cost_id', {})

            # Convertir claves de string a int en los diccionarios
            self._next_person_id = {int(k): v for k, v in self._next_person_id.items()}
            self._next_item_id = {int(k): v for k, v in self._next_item_id.items()}
            self._next_shared_cost_id = {int(k): v for k, v in self._next_shared_cost_id.items()}

            # Cargar trip_data
            self.trip_data = {}
            for trip_id_str, trip_content in data.get('trip_data', {}).items():
                trip_id = int(trip_id_str)
                self.trip_data[trip_id] = {
                    'persons': [self._dict_to_person(p) for p in trip_content.get('persons', [])],
                    'items': [self._dict_to_item(i) for i in trip_content.get('items', [])],
                    'shared_costs': [self._dict_to_shared_cost(sc) for sc in trip_content.get('shared_costs', [])]
                }

            print(f"✓ Datos cargados desde {self.DATA_FILE} ({len(self.trips)} viajes)")
        except Exception as e:
            print(f"✗ Error al cargar datos: {e}")
            print("Iniciando con datos vacíos.")

    # Métodos auxiliares para serialización
    def _trip_to_dict(self, trip: Trip) -> dict:
        return {
            'id': trip.id,
            'name': trip.name,
            'description': trip.description,
            'days': trip.days,
            'created_at': trip.created_at.isoformat()
        }

    def _dict_to_trip(self, data: dict) -> Trip:
        return Trip(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            days=data.get('days', 1),
            created_at=datetime.fromisoformat(data['created_at'])
        )

    def _person_to_dict(self, person: Person) -> dict:
        return {'id': person.id, 'name': person.name}

    def _dict_to_person(self, data: dict) -> Person:
        return Person(id=data['id'], name=data['name'])

    def _item_to_dict(self, item: Item) -> dict:
        return {
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'day': item.day,
            'url': item.url,
            'person_ids': list(item.person_ids),
            'paid_by_person_id': item.paid_by_person_id
        }

    def _dict_to_item(self, data: dict) -> Item:
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

    def _shared_cost_to_dict(self, sc: SharedCost) -> dict:
        return {
            'id': sc.id,
            'name': sc.name,
            'cost': sc.cost,
            'day': sc.day
        }

    def _dict_to_shared_cost(self, data: dict) -> SharedCost:
        return SharedCost(
            id=data['id'],
            name=data['name'],
            cost=data['cost'],
            day=data.get('day', 1)
        )

    # Gestión de viajes
    def add_trip(self, name: str, description: str = "", days: int = 1) -> Trip:
        if self.use_firestore:
            return self._store.add_trip(name, description, days)

        trip = Trip(id=self._next_trip_id, name=name, description=description, days=days)
        self.trips.append(trip)
        self.trip_data[trip.id] = {
            'persons': [],
            'items': [],
            'shared_costs': []
        }
        self._next_person_id[trip.id] = 1
        self._next_item_id[trip.id] = 1
        self._next_shared_cost_id[trip.id] = 1
        self._next_trip_id += 1
        self.save_to_file()  # Guardar cambios
        return trip

    def get_trip(self, trip_id: int) -> Optional[Trip]:
        if self.use_firestore:
            return self._store.get_trip(trip_id)

        for trip in self.trips:
            if trip.id == trip_id:
                return trip
        return None

    def set_current_trip(self, trip_id: int) -> bool:
        if self.use_firestore:
            result = self._store.set_current_trip(trip_id)
            if result:
                self.current_trip_id = trip_id
            return result

        if self.get_trip(trip_id):
            self.current_trip_id = trip_id
            return True
        return False

    def remove_trip(self, trip_id: int) -> bool:
        if self.use_firestore:
            result = self._store.remove_trip(trip_id)
            if result and self.current_trip_id == trip_id:
                self.current_trip_id = None
            return result

        trip = self.get_trip(trip_id)
        if trip:
            self.trips.remove(trip)
            if trip_id in self.trip_data:
                del self.trip_data[trip_id]
            if self.current_trip_id == trip_id:
                self.current_trip_id = None
            self.save_to_file()  # Guardar cambios
            return True
        return False

    # Propiedades de acceso rápido al viaje actual
    @property
    def trips(self) -> List[Trip]:
        if self.use_firestore:
            return self._store.list_trips()
        return self._trips_list if hasattr(self, '_trips_list') else []

    @trips.setter
    def trips(self, value: List[Trip]):
        if not self.use_firestore:
            self._trips_list = value

    @property
    def persons(self) -> List[Person]:
        if self.use_firestore:
            if self.current_trip_id:
                return self._store.list_persons(self.current_trip_id)
            return []

        if self.current_trip_id and self.current_trip_id in self.trip_data:
            return self.trip_data[self.current_trip_id]['persons']
        return []

    @property
    def items(self) -> List[Item]:
        if self.use_firestore:
            if self.current_trip_id:
                return self._store.list_items(self.current_trip_id)
            return []

        if self.current_trip_id and self.current_trip_id in self.trip_data:
            return self.trip_data[self.current_trip_id]['items']
        return []

    @property
    def shared_costs(self) -> List[SharedCost]:
        if self.use_firestore:
            if self.current_trip_id:
                return self._store.list_shared_costs(self.current_trip_id)
            return []

        if self.current_trip_id and self.current_trip_id in self.trip_data:
            return self.trip_data[self.current_trip_id]['shared_costs']
        return []

    def get_items_by_day(self, day: int) -> List[Item]:
        """Obtiene los ítems de un día específico"""
        if self.use_firestore:
            if self.current_trip_id:
                return self._store.get_items_by_day(self.current_trip_id, day)
            return []

        return [item for item in self.items if item.day == day]

    def get_shared_costs_by_day(self, day: int) -> List[SharedCost]:
        """Obtiene los costos compartidos de un día específico"""
        if self.use_firestore:
            if self.current_trip_id:
                return self._store.get_shared_costs_by_day(self.current_trip_id, day)
            return []

        return [sc for sc in self.shared_costs if sc.day == day]

    # Gestión de personas
    def add_person(self, name: str) -> Optional[Person]:
        if not self.current_trip_id:
            return None

        if self.use_firestore:
            return self._store.add_person(self.current_trip_id, name)

        person = Person(id=self._next_person_id[self.current_trip_id], name=name)
        self.persons.append(person)
        self._next_person_id[self.current_trip_id] += 1
        self.save_to_file()
        return person

    def remove_person(self, person_id: int) -> bool:
        if self.use_firestore:
            if not self.current_trip_id:
                return False
            return self._store.remove_person(self.current_trip_id, person_id)

        person = self.get_person(person_id)
        if person:
            self.persons.remove(person)
            # Remover de todos los ítems
            for item in self.items:
                item.person_ids.discard(person_id)
            self.save_to_file()
            return True
        return False

    def get_person(self, person_id: int) -> Optional[Person]:
        if self.use_firestore:
            if not self.current_trip_id:
                return None
            return self._store.get_person(self.current_trip_id, person_id)

        for person in self.persons:
            if person.id == person_id:
                return person
        return None

    # Gestión de ítems
    def add_item(self, name: str, quantity: int, unit_price: float, day: int = 1, url: str = "", paid_by_person_id: int = None) -> Optional[Item]:
        if not self.current_trip_id:
            return None

        if self.use_firestore:
            return self._store.add_item(self.current_trip_id, name, quantity, unit_price, day, url, paid_by_person_id)

        item = Item(id=self._next_item_id[self.current_trip_id], name=name, quantity=quantity,
                   unit_price=unit_price, day=day, url=url, paid_by_person_id=paid_by_person_id)
        self.items.append(item)
        self._next_item_id[self.current_trip_id] += 1
        self.save_to_file()
        return item

    def remove_item(self, item_id: int) -> bool:
        if self.use_firestore:
            if not self.current_trip_id:
                return False
            return self._store.remove_item(self.current_trip_id, item_id)

        item = self.get_item(item_id)
        if item:
            self.items.remove(item)
            self.save_to_file()
            return True
        return False

    def update_item(self, item_id: int, name: str = None, quantity: int = None,
                   unit_price: float = None, day: int = None, url: str = None,
                   paid_by_person_id: int = None) -> bool:
        """Actualiza un ítem existente"""
        if self.use_firestore:
            if not self.current_trip_id:
                return False
            return self._store.update_item(
                self.current_trip_id, item_id,
                name=name, quantity=quantity, unit_price=unit_price,
                day=day, url=url, paid_by_person_id=paid_by_person_id
            )

        item = self.get_item(item_id)
        if item:
            if name is not None:
                item.name = name
            if quantity is not None:
                item.quantity = quantity
            if unit_price is not None:
                item.unit_price = unit_price
            if day is not None:
                item.day = day
            if url is not None:
                item.url = url
            if paid_by_person_id is not None:
                item.paid_by_person_id = paid_by_person_id
            self.save_to_file()
            return True
        return False

    def get_item(self, item_id: int) -> Optional[Item]:
        if self.use_firestore:
            if not self.current_trip_id:
                return None
            return self._store.get_item(self.current_trip_id, item_id)

        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def toggle_person_for_item(self, item_id: int, person_id: int) -> bool:
        """Alterna la participación de una persona en un ítem"""
        if self.use_firestore:
            if not self.current_trip_id:
                return False
            return self._store.toggle_person_for_item(self.current_trip_id, item_id, person_id)

        item = self.get_item(item_id)
        if item and self.get_person(person_id):
            if person_id in item.person_ids:
                item.person_ids.remove(person_id)
            else:
                item.person_ids.add(person_id)
            self.save_to_file()
            return True
        return False

    # Gestión de costos compartidos
    def add_shared_cost(self, name: str, cost: float, day: int = 1) -> Optional[SharedCost]:
        if not self.current_trip_id:
            return None

        if self.use_firestore:
            return self._store.add_shared_cost(self.current_trip_id, name, cost, day)

        shared_cost = SharedCost(id=self._next_shared_cost_id[self.current_trip_id], name=name, cost=cost, day=day)
        self.shared_costs.append(shared_cost)
        self._next_shared_cost_id[self.current_trip_id] += 1
        self.save_to_file()
        return shared_cost

    def remove_shared_cost(self, shared_cost_id: int) -> bool:
        if self.use_firestore:
            if not self.current_trip_id:
                return False
            return self._store.remove_shared_cost(self.current_trip_id, shared_cost_id)

        shared_cost = self.get_shared_cost(shared_cost_id)
        if shared_cost:
            self.shared_costs.remove(shared_cost)
            self.save_to_file()
            return True
        return False

    def get_shared_cost(self, shared_cost_id: int) -> Optional[SharedCost]:
        if self.use_firestore:
            if not self.current_trip_id:
                return None
            return self._store.get_shared_cost(self.current_trip_id, shared_cost_id)

        for shared_cost in self.shared_costs:
            if shared_cost.id == shared_cost_id:
                return shared_cost
        return None

    def clear_all(self):
        """Limpia todos los datos del viaje actual"""
        if not self.current_trip_id:
            return

        if self.use_firestore:
            self._store.clear_trip_data(self.current_trip_id)
            return

        if self.current_trip_id in self.trip_data:
            self.trip_data[self.current_trip_id] = {
                'persons': [],
                'items': [],
                'shared_costs': []
            }
            self._next_person_id[self.current_trip_id] = 1
            self._next_item_id[self.current_trip_id] = 1
            self._next_shared_cost_id[self.current_trip_id] = 1
            self.save_to_file()


