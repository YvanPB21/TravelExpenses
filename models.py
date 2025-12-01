"""
Modelos de datos para la aplicación de división de gastos
"""
from typing import List, Set, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Trip:
    """Representa un viaje o evento de gastos compartidos"""
    id: int
    name: str
    description: str = ""
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
    url: str = ""  # URL del producto (opcional)
    person_ids: Set[int] = field(default_factory=set)  # IDs de personas que participan

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


class DataStore:
    """Almacena todos los datos en memoria, organizados por viajes"""

    def __init__(self):
        self.trips: List[Trip] = []
        self.current_trip_id: int = None
        # Datos por viaje: {trip_id: {'persons': [], 'items': [], 'shared_costs': []}}
        self.trip_data: Dict[int, Dict] = {}
        self._next_trip_id = 1
        self._next_person_id = {}  # {trip_id: next_id}
        self._next_item_id = {}
        self._next_shared_cost_id = {}

    # Gestión de viajes
    def add_trip(self, name: str, description: str = "") -> Trip:
        trip = Trip(id=self._next_trip_id, name=name, description=description)
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
        return trip

    def get_trip(self, trip_id: int) -> Trip:
        for trip in self.trips:
            if trip.id == trip_id:
                return trip
        return None

    def set_current_trip(self, trip_id: int) -> bool:
        if self.get_trip(trip_id):
            self.current_trip_id = trip_id
            return True
        return False

    def remove_trip(self, trip_id: int) -> bool:
        trip = self.get_trip(trip_id)
        if trip:
            self.trips.remove(trip)
            if trip_id in self.trip_data:
                del self.trip_data[trip_id]
            if self.current_trip_id == trip_id:
                self.current_trip_id = None
            return True
        return False

    # Propiedades de acceso rápido al viaje actual
    @property
    def persons(self) -> List[Person]:
        if self.current_trip_id and self.current_trip_id in self.trip_data:
            return self.trip_data[self.current_trip_id]['persons']
        return []

    @property
    def items(self) -> List[Item]:
        if self.current_trip_id and self.current_trip_id in self.trip_data:
            return self.trip_data[self.current_trip_id]['items']
        return []

    @property
    def shared_costs(self) -> List[SharedCost]:
        if self.current_trip_id and self.current_trip_id in self.trip_data:
            return self.trip_data[self.current_trip_id]['shared_costs']
        return []

    # Gestión de personas
    def add_person(self, name: str) -> Person:
        if not self.current_trip_id:
            return None
        person = Person(id=self._next_person_id[self.current_trip_id], name=name)
        self.persons.append(person)
        self._next_person_id[self.current_trip_id] += 1
        return person

    def remove_person(self, person_id: int) -> bool:
        person = self.get_person(person_id)
        if person:
            self.persons.remove(person)
            # Remover de todos los ítems
            for item in self.items:
                item.person_ids.discard(person_id)
            return True
        return False

    def get_person(self, person_id: int) -> Person:
        for person in self.persons:
            if person.id == person_id:
                return person
        return None

    # Gestión de ítems
    def add_item(self, name: str, quantity: int, unit_price: float, url: str = "") -> Item:
        if not self.current_trip_id:
            return None
        item = Item(id=self._next_item_id[self.current_trip_id], name=name, quantity=quantity, unit_price=unit_price, url=url)
        self.items.append(item)
        self._next_item_id[self.current_trip_id] += 1
        return item

    def remove_item(self, item_id: int) -> bool:
        item = self.get_item(item_id)
        if item:
            self.items.remove(item)
            return True
        return False

    def get_item(self, item_id: int) -> Item:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def toggle_person_for_item(self, item_id: int, person_id: int) -> bool:
        """Alterna la participación de una persona en un ítem"""
        item = self.get_item(item_id)
        if item and self.get_person(person_id):
            if person_id in item.person_ids:
                item.person_ids.remove(person_id)
            else:
                item.person_ids.add(person_id)
            return True
        return False

    # Gestión de costos compartidos
    def add_shared_cost(self, name: str, cost: float) -> SharedCost:
        if not self.current_trip_id:
            return None
        shared_cost = SharedCost(id=self._next_shared_cost_id[self.current_trip_id], name=name, cost=cost)
        self.shared_costs.append(shared_cost)
        self._next_shared_cost_id[self.current_trip_id] += 1
        return shared_cost

    def remove_shared_cost(self, shared_cost_id: int) -> bool:
        shared_cost = self.get_shared_cost(shared_cost_id)
        if shared_cost:
            self.shared_costs.remove(shared_cost)
            return True
        return False

    def get_shared_cost(self, shared_cost_id: int) -> SharedCost:
        for shared_cost in self.shared_costs:
            if shared_cost.id == shared_cost_id:
                return shared_cost
        return None

    def clear_all(self):
        """Limpia todos los datos del viaje actual"""
        if self.current_trip_id and self.current_trip_id in self.trip_data:
            self.trip_data[self.current_trip_id] = {
                'persons': [],
                'items': [],
                'shared_costs': []
            }
            self._next_person_id[self.current_trip_id] = 1
            self._next_item_id[self.current_trip_id] = 1
            self._next_shared_cost_id[self.current_trip_id] = 1

