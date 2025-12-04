"""
Lógica de cálculo para división de gastos con soporte por días
"""
from typing import Dict, List
from models import DataStore


class BillCalculator:
    """Calcula cuánto debe pagar cada persona"""

    def __init__(self, data_store: DataStore):
        self.data_store = data_store

    def calculate_totals_by_day(self, day: int) -> Dict[int, Dict[str, float]]:
        """
        Calcula el total que debe pagar cada persona en un día específico

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

        # Calcular costos de ítems individuales del día
        items_day = self.data_store.get_items_by_day(day)
        for item in items_day:
            if len(item.person_ids) > 0:
                cost_per_person = item.total_cost / len(item.person_ids)
                for person_id in item.person_ids:
                    if person_id in totals:
                        totals[person_id]['items_total'] += cost_per_person

        # Los costos compartidos ya no se calculan por día
        # Se calculan en el total general

        # Calcular total del día (solo items)
        for person_id in totals:
            totals[person_id]['total'] = totals[person_id]['items_total']

        return totals

    def calculate_totals(self) -> Dict[int, Dict[str, float]]:
        """
        Calcula el total general que debe pagar cada persona (todos los días)

        Returns:
            Dict con {person_id: {
                'items_total': float,
                'shared_total': float,
                'total': float,
                'by_day': {day: total}
            }}
        """
        current_trip = self.data_store.get_trip(self.data_store.current_trip_id)
        if not current_trip:
            return {}

        # Inicializar totales generales
        totals = {}
        for person in self.data_store.persons:
            totals[person.id] = {
                'items_total': 0.0,
                'shared_total': 0.0,
                'total': 0.0,
                'by_day': {}
            }

        # Calcular para cada día (solo items)
        for day in range(1, current_trip.days + 1):
            day_totals = self.calculate_totals_by_day(day)
            for person_id, amounts in day_totals.items():
                if person_id in totals:
                    totals[person_id]['items_total'] += amounts['items_total']
                    totals[person_id]['by_day'][day] = amounts['items_total']

        # Calcular costos compartidos (aplicados al total general)
        if len(self.data_store.persons) > 0:
            total_shared = sum(sc.cost for sc in self.data_store.shared_costs)
            shared_per_person = total_shared / len(self.data_store.persons)

            for person_id in totals:
                totals[person_id]['shared_total'] = shared_per_person

        # Calcular total final
        for person_id in totals:
            totals[person_id]['total'] = (
                totals[person_id]['items_total'] +
                totals[person_id]['shared_total']
            )

        return totals

    def get_day_total(self, day: int) -> float:
        """Calcula el total de gastos de un día específico (solo items)"""
        items_day = self.data_store.get_items_by_day(day)
        items_total = sum(item.total_cost for item in items_day)
        return items_total

    def get_grand_total(self) -> float:
        """Calcula el total general de todos los gastos"""
        items_total = sum(item.total_cost for item in self.data_store.items)
        shared_total = sum(sc.cost for sc in self.data_store.shared_costs)
        return items_total + shared_total

    def get_summary(self) -> Dict[str, float]:
        """
        Calcula un resumen completo con verificación

        Returns:
            Dict con verificación de balance
        """
        totals = self.calculate_totals()

        total_items = sum(item.total_cost for item in self.data_store.items)
        total_shared = sum(sc.cost for sc in self.data_store.shared_costs)
        grand_total = total_items + total_shared

        # Sumar lo que deben todas las personas
        total_distributed = sum(person_total['total'] for person_total in totals.values())

        # La diferencia debería ser 0 (o muy cercana a 0 por redondeo)
        difference = abs(grand_total - total_distributed)

        return {
            'total_items': total_items,
            'total_shared': total_shared,
            'grand_total': grand_total,
            'total_distributed': total_distributed,
            'difference': difference,
            'is_balanced': difference < 0.01
        }

    def calculate_payments_summary(self) -> Dict[int, Dict[str, float]]:
        """
        Calcula cuánto pagó cada persona y cuánto se le debe devolver

        Returns:
            Dict con {person_id: {
                'total_paid': float,      # Lo que pagó
                'total_owes': float,      # Lo que debe (su consumo)
                'balance': float          # Positivo = le deben, Negativo = debe
            }}
        """
        totals = self.calculate_totals()
        payments = {}

        for person in self.data_store.persons:
            # Calcular lo que pagó esta persona
            total_paid = 0.0
            
            # Sumar items pagados
            for item in self.data_store.items:
                if item.paid_by_person_id == person.id:
                    total_paid += item.total_cost

            # Sumar costos compartidos pagados (dividido equitativamente)
            for shared_cost in self.data_store.shared_costs:
                if person.id in shared_cost.paid_by_person_ids:
                    # Dividir el costo entre el número de personas que pagaron
                    num_payers = len(shared_cost.paid_by_person_ids)
                    if num_payers > 0:
                        total_paid += shared_cost.cost / num_payers

            # Lo que debe (su consumo total)
            total_owes = totals.get(person.id, {}).get('total', 0.0)

            # Balance: positivo = le deben, negativo = debe
            balance = total_paid - total_owes

            payments[person.id] = {
                'total_paid': total_paid,
                'total_owes': total_owes,
                'balance': balance
            }

        return payments

