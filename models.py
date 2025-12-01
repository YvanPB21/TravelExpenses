"""
Modelos de datos para la aplicación de división de gastos
"""
from typing import List, Set
from dataclasses import dataclass, field


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
    cost: float
    person_ids: Set[int] = field(default_factory=set)  # IDs de personas que participan


@dataclass
class SharedCost:
    """Representa un costo compartido por todos"""
    id: int
    name: str
    cost: float


class DataStore:
    """Almacena todos los datos en memoria"""

    def __init__(self):
        self.persons: List[Person] = []
        self.items: List[Item] = []
        self.shared_costs: List[SharedCost] = []
        self._next_person_id = 1
        self._next_item_id = 1
        self._next_shared_cost_id = 1

    # Gestión de personas
    def add_person(self, name: str) -> Person:
        person = Person(id=self._next_person_id, name=name)
        self.persons.append(person)
        self._next_person_id += 1
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
    def add_item(self, name: str, cost: float) -> Item:
        item = Item(id=self._next_item_id, name=name, cost=cost)
        self.items.append(item)
        self._next_item_id += 1
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
        shared_cost = SharedCost(id=self._next_shared_cost_id, name=name, cost=cost)
        self.shared_costs.append(shared_cost)
        self._next_shared_cost_id += 1
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
        """Limpia todos los datos"""
        self.persons.clear()
        self.items.clear()
        self.shared_costs.clear()
        self._next_person_id = 1
        self._next_item_id = 1
        self._next_shared_cost_id = 1

