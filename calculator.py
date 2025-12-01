"""
Lógica de cálculo para división de gastos
"""
from typing import Dict
from models import DataStore


class BillCalculator:
    """Calcula cuánto debe pagar cada persona"""

    def __init__(self, data_store: DataStore):
        self.data_store = data_store

    def calculate_totals(self) -> Dict[int, Dict[str, float]]:
        """
        Calcula el total que debe pagar cada persona

        Returns:
            Dict con {person_id: {
                'items_total': float,
                'shared_total': float,
                'total': float
            }}
        """
        # Inicializar totales para cada persona
        totals = {}
        for person in self.data_store.persons:
            totals[person.id] = {
                'items_total': 0.0,
                'shared_total': 0.0,
                'total': 0.0
            }

        # Calcular costos de ítems individuales
        for item in self.data_store.items:
            if len(item.person_ids) > 0:
                cost_per_person = item.cost / len(item.person_ids)
                for person_id in item.person_ids:
                    if person_id in totals:
                        totals[person_id]['items_total'] += cost_per_person

        # Calcular costos compartidos
        if len(self.data_store.persons) > 0:
            total_shared = sum(sc.cost for sc in self.data_store.shared_costs)
            shared_per_person = total_shared / len(self.data_store.persons)

            for person_id in totals:
                totals[person_id]['shared_total'] = shared_per_person

        # Calcular total
        for person_id in totals:
            totals[person_id]['total'] = (
                totals[person_id]['items_total'] +
                totals[person_id]['shared_total']
            )

        return totals

    def get_grand_total(self) -> float:
        """Calcula el total general de todos los gastos"""
        items_total = sum(item.cost for item in self.data_store.items)
        shared_total = sum(sc.cost for sc in self.data_store.shared_costs)
        return items_total + shared_total

