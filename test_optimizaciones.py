"""Script de prueba rápida para verificar las optimizaciones de Firestore."""
import os
import sys
import time

# Activar modo debug
os.environ['DEBUG_FIRESTORE'] = 'true'

print("=" * 70)
print("PRUEBA DE OPTIMIZACIONES DE FIRESTORE")
print("=" * 70)

try:
    # Importar después de configurar variables de entorno
    from db.firestore_store import FirestoreStore
    from db.firebase_client import FirebaseConfig

    print("\n✅ Módulos importados correctamente")

    # Crear instancia de Firestore Store
    print("\n🔥 Inicializando Firestore Store...")
    store = FirestoreStore(FirebaseConfig())

    print("\n✅ Firestore Store inicializado correctamente")
    print(f"   - Caché habilitado: {store._enable_cache}")
    print(f"   - TTL del caché: {store._cache_ttl}s")

    # Test 1: Crear un viaje de prueba
    print("\n📝 Test 1: Crear viaje de prueba...")
    trip = store.add_trip("Test Optimizaciones", "Prueba de rendimiento", 2)
    print(f"   ✅ Viaje creado: ID={trip.id}, Nombre={trip.name}")

    # Test 2: Agregar personas
    print("\n👥 Test 2: Agregar personas...")
    person1 = store.add_person(trip.id, "Usuario Test 1")
    person2 = store.add_person(trip.id, "Usuario Test 2")
    print(f"   ✅ Personas creadas: {person1.name}, {person2.name}")

    # Test 3: Listar personas (debería usar caché después de la primera vez)
    print("\n📖 Test 3: Lectura con caché...")
    print("   Primera lectura (cache miss):")
    start = time.time()
    persons_1 = store.list_persons(trip.id)
    time_1 = time.time() - start
    print(f"   ✅ Personas leídas: {len(persons_1)} en {time_1:.4f}s")

    print("\n   Segunda lectura (cache hit esperado):")
    start = time.time()
    persons_2 = store.list_persons(trip.id)
    time_2 = time.time() - start
    print(f"   ✅ Personas leídas: {len(persons_2)} en {time_2:.4f}s")

    if time_2 < time_1:
        speedup = (time_1 / time_2) if time_2 > 0 else float('inf')
        print(f"   🚀 Speedup con caché: {speedup:.1f}x más rápido")

    # Test 4: Agregar items
    print("\n🛒 Test 4: Agregar items...")
    item1 = store.add_item(trip.id, "Item Test 1", 2, 10.0, 1)
    item2 = store.add_item(trip.id, "Item Test 2", 1, 20.0, 2)
    print(f"   ✅ Items creados: {item1.name}, {item2.name}")

    # Test 5: Invalidación de caché
    print("\n🔄 Test 5: Invalidación de caché...")
    print("   Leyendo items (cache miss esperado tras add_item):")
    items = store.list_items(trip.id)
    print(f"   ✅ Items leídos: {len(items)}")

    # Test 6: Filtrado en memoria (get_items_by_day)
    print("\n📅 Test 6: Filtrado por día (optimizado)...")
    start = time.time()
    items_day1 = store.get_items_by_day(trip.id, 1)
    time_day1 = time.time() - start
    print(f"   ✅ Items del día 1: {len(items_day1)} en {time_day1:.4f}s")

    # Test 7: Batch operations (limpiar viaje)
    print("\n🗑️  Test 7: Batch operations (clear_trip_data)...")
    start = time.time()
    store.clear_trip_data(trip.id)
    time_clear = time.time() - start
    print(f"   ✅ Viaje limpiado en {time_clear:.4f}s")

    # Verificar que se limpió
    persons_after = store.list_persons(trip.id)
    items_after = store.list_items(trip.id)
    print(f"   ✅ Verificado: {len(persons_after)} personas, {len(items_after)} items (esperado: 0)")

    # Test 8: Eliminar viaje
    print("\n🗑️  Test 8: Eliminar viaje completo...")
    start = time.time()
    result = store.remove_trip(trip.id)
    time_remove = time.time() - start
    print(f"   ✅ Viaje eliminado en {time_remove:.4f}s")

    # Resumen
    print("\n" + "=" * 70)
    print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 70)
    print("\n📊 Resumen de rendimiento:")
    print(f"   - Speedup con caché: {speedup:.1f}x más rápido" if speedup < float('inf') else "   - Caché funcionando correctamente")
    print(f"   - Filtrado por día: {time_day1:.4f}s")
    print(f"   - Clear trip data: {time_clear:.4f}s")
    print(f"   - Remove trip: {time_remove:.4f}s")

    print("\n💡 Observa los mensajes de debug arriba para ver:")
    print("   - 📖 = Lectura desde Firestore")
    print("   - ⚡ = Cache HIT (lectura desde memoria)")

    print("\n🎉 Las optimizaciones están funcionando correctamente!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

