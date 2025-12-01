"""
Script de prueba para verificar la funcionalidad del sistema
"""
from models import DataStore
from calculator import BillCalculator


def test_basic_functionality():
    """Prueba básica de funcionalidad"""
    print("=== Prueba de Funcionalidad Split Bill ===\n")

    # Crear data store y calculadora
    store = DataStore()
    calc = BillCalculator(store)

    # Agregar personas
    print("1. Agregando personas...")
    ana = store.add_person("Ana")
    juan = store.add_person("Juan")
    maria = store.add_person("María")
    print(f"   ✓ {ana.name}, {juan.name}, {maria.name}")

    # Agregar ítems
    print("\n2. Agregando ítems de compra...")
    pizza = store.add_item("Pizza", 2, 15.0)  # 2 pizzas a $15 cada una = $30
    print(f"   ✓ {pizza.name}: {pizza.quantity}x ${pizza.unit_price} = ${pizza.total_cost}")

    ensalada = store.add_item("Ensalada", 1, 15.0)  # 1 ensalada a $15 = $15
    print(f"   ✓ {ensalada.name}: {ensalada.quantity}x ${ensalada.unit_price} = ${ensalada.total_cost}")

    refresco = store.add_item("Refresco", 3, 3.33)  # 3 refrescos a $3.33 cada uno ≈ $10
    print(f"   ✓ {refresco.name}: {refresco.quantity}x ${refresco.unit_price} = ${refresco.total_cost:.2f}")

    # Asignar personas a ítems
    print("\n3. Asignando personas a ítems...")
    store.toggle_person_for_item(pizza.id, ana.id)
    store.toggle_person_for_item(pizza.id, juan.id)
    print(f"   ✓ Pizza: Ana y Juan")

    store.toggle_person_for_item(ensalada.id, maria.id)
    print(f"   ✓ Ensalada: María")

    store.toggle_person_for_item(refresco.id, ana.id)
    store.toggle_person_for_item(refresco.id, juan.id)
    store.toggle_person_for_item(refresco.id, maria.id)
    print(f"   ✓ Refresco: Ana, Juan y María")

    # Agregar costos compartidos
    print("\n4. Agregando costos compartidos...")
    propina = store.add_shared_cost("Propina", 15.0)
    print(f"   ✓ {propina.name}: ${propina.cost}")

    # Calcular totales
    print("\n5. Calculando totales...")
    totals = calc.calculate_totals()
    grand_total = calc.get_grand_total()

    print("\n=== RESUMEN DE PAGOS ===")
    print("-" * 60)
    print(f"{'Persona':<15} {'Ítems':<15} {'Compartido':<15} {'Total':<15}")
    print("-" * 60)

    for person in store.persons:
        person_totals = totals[person.id]
        print(f"{person.name:<15} "
              f"${person_totals['items_total']:<14.2f} "
              f"${person_totals['shared_total']:<14.2f} "
              f"${person_totals['total']:<14.2f}")

    print("-" * 60)
    print(f"{'TOTAL GENERAL':<45} ${grand_total:.2f}")
    print("-" * 60)

    # Verificaciones
    print("\n=== Verificaciones ===")
    # Usar comparación aproximada para evitar problemas de precisión
    assert abs(totals[ana.id]['items_total'] - 18.33) < 0.01, "Error en cálculo de Ana (ítems)"
    assert abs(totals[juan.id]['items_total'] - 18.33) < 0.01, "Error en cálculo de Juan (ítems)"
    assert abs(totals[maria.id]['items_total'] - 18.33) < 0.01, "Error en cálculo de María (ítems)"

    for person in store.persons:
        assert abs(totals[person.id]['shared_total'] - 5.0) < 0.01, f"Error en cálculo de costos compartidos para {person.name}"

    assert abs(grand_total - 70.0) < 0.01, "Error en total general"

    print("✓ Todas las verificaciones pasaron correctamente!")
    print("\n✅ Sistema funcionando correctamente!")


if __name__ == '__main__':
    test_basic_functionality()

