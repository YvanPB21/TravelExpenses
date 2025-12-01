"""Script para migrar datos desde JSON local a Firebase Firestore."""
import json
import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.firebase_client import FirebaseConfig
from db.firestore_store import FirestoreStore


def migrate_json_to_firestore(json_file: str = 'split_bill_data.json',
                               credentials_path: str = None,
                               dry_run: bool = False):
    """
    Migra datos desde el archivo JSON a Firestore.

    Args:
        json_file: Ruta al archivo JSON
        credentials_path: Ruta al archivo de credenciales de Firebase
        dry_run: Si True, solo muestra qué se migrará sin hacerlo
    """
    print("=" * 60)
    print("MIGRACIÓN DE JSON A FIRESTORE")
    print("=" * 60)

    # Verificar que existe el archivo JSON
    if not os.path.exists(json_file):
        print(f"❌ Error: No se encuentra el archivo {json_file}")
        return False

    # Cargar datos del JSON
    print(f"\n📂 Cargando datos desde {json_file}...")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer JSON: {e}")
        return False

    trips = data.get('trips', [])
    trip_data = data.get('trip_data', {})
    current_trip_id = data.get('current_trip_id')

    print(f"✓ Datos cargados: {len(trips)} viajes")

    if dry_run:
        print("\n🔍 MODO DRY-RUN (solo vista previa, no se migrarán datos)")

    # Inicializar Firestore
    print(f"\n🔥 Conectando a Firestore...")
    try:
        config = FirebaseConfig(credentials_path=credentials_path) if credentials_path else FirebaseConfig()
        store = FirestoreStore(config)
        print("✓ Conectado a Firestore")
    except Exception as e:
        print(f"❌ Error al conectar a Firestore: {e}")
        print("\nAsegúrate de:")
        print("  1. Tener las credenciales de Firebase configuradas")
        print("  2. Haber instalado firebase-admin: pip install firebase-admin")
        return False

    if dry_run:
        print("\n📋 RESUMEN DE LO QUE SE MIGRARÁ:")
        for trip in trips:
            print(f"\n  Viaje: {trip['name']} (ID: {trip['id']})")
            trip_id = str(trip['id'])
            if trip_id in trip_data:
                td = trip_data[trip_id]
                print(f"    - Personas: {len(td.get('persons', []))}")
                print(f"    - Items: {len(td.get('items', []))}")
                print(f"    - Costos compartidos: {len(td.get('shared_costs', []))}")

        if current_trip_id:
            print(f"\n  Viaje actual: ID {current_trip_id}")

        print("\n✓ Vista previa completa. Ejecuta sin --dry-run para migrar.")
        return True

    # Migrar datos reales
    print("\n🚀 Iniciando migración...")
    migrated_trips = 0
    migrated_persons = 0
    migrated_items = 0
    migrated_shared = 0

    try:
        # Migrar cada viaje
        for trip_json in trips:
            trip_id = trip_json['id']
            print(f"\n  Migrando viaje: {trip_json['name']} (ID: {trip_id})...")

            # Crear viaje en Firestore
            # Nota: usamos el ID del JSON para mantener consistencia
            from models import Trip
            trip = Trip(
                id=trip_id,
                name=trip_json['name'],
                description=trip_json.get('description', ''),
                days=trip_json.get('days', 1),
                created_at=datetime.fromisoformat(trip_json['created_at'])
            )

            # Guardar directamente en Firestore
            trip_data_dict = {
                'id': trip.id,
                'name': trip.name,
                'description': trip.description,
                'days': trip.days,
                'created_at': trip.created_at.isoformat()
            }
            store._trips.document(str(trip_id)).set(trip_data_dict)
            store._init_trip_counters(trip_id)
            migrated_trips += 1

            # Migrar datos del viaje
            trip_id_str = str(trip_id)
            if trip_id_str in trip_data:
                td = trip_data[trip_id_str]

                # Migrar personas
                for person_json in td.get('persons', []):
                    person_data = {
                        'trip_id': trip_id,
                        'id': person_json['id'],
                        'name': person_json['name']
                    }
                    store._persons.document(f"{trip_id}_{person_json['id']}").set(person_data)
                    migrated_persons += 1

                # Migrar items
                for item_json in td.get('items', []):
                    item_data = {
                        'trip_id': trip_id,
                        'id': item_json['id'],
                        'name': item_json['name'],
                        'quantity': item_json['quantity'],
                        'unit_price': item_json['unit_price'],
                        'day': item_json.get('day', 1),
                        'url': item_json.get('url', ''),
                        'person_ids': item_json.get('person_ids', []),
                        'paid_by_person_id': item_json.get('paid_by_person_id')
                    }
                    store._items.document(f"{trip_id}_{item_json['id']}").set(item_data)
                    migrated_items += 1

                # Migrar costos compartidos
                for sc_json in td.get('shared_costs', []):
                    sc_data = {
                        'trip_id': trip_id,
                        'id': sc_json['id'],
                        'name': sc_json['name'],
                        'cost': sc_json['cost'],
                        'day': sc_json.get('day', 1)
                    }
                    store._shared_costs.document(f"{trip_id}_{sc_json['id']}").set(sc_data)
                    migrated_shared += 1

                print(f"    ✓ {migrated_persons} personas, {migrated_items} items, {migrated_shared} costos compartidos")

        # Establecer viaje actual
        if current_trip_id:
            store._set_current_trip_id(current_trip_id)
            print(f"\n  ✓ Viaje actual establecido: ID {current_trip_id}")

        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA")
        print("=" * 60)
        print(f"  Viajes migrados: {migrated_trips}")
        print(f"  Personas migradas: {migrated_persons}")
        print(f"  Items migrados: {migrated_items}")
        print(f"  Costos compartidos migrados: {migrated_shared}")
        print("\n💡 Ahora puedes ejecutar la aplicación con Firestore.")
        print("   Los datos del JSON han sido migrados exitosamente.")

        return True

    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Migrar datos de JSON a Firestore')
    parser.add_argument('--json-file', default='split_bill_data.json',
                       help='Ruta al archivo JSON (default: split_bill_data.json)')
    parser.add_argument('--credentials', help='Ruta al archivo de credenciales de Firebase')
    parser.add_argument('--dry-run', action='store_true',
                       help='Solo mostrar qué se migrará, sin migrar')

    args = parser.parse_args()

    success = migrate_json_to_firestore(
        json_file=args.json_file,
        credentials_path=args.credentials,
        dry_run=args.dry_run
    )

    sys.exit(0 if success else 1)

