"""
Script para ayudarte a configurar el nombre de la base de datos de Firestore.
"""

print("=" * 60)
print("CONFIGURACIÓN DE FIRESTORE DATABASE ID")
print("=" * 60)
print()
print("Instrucciones:")
print("1. Ve a Firebase Console: https://console.firebase.google.com/")
print("2. Selecciona tu proyecto: travelexpenses-301bc")
print("3. Ve a 'Firestore Database'")
print()
print("Si ves un mensaje para crear la base de datos:")
print("  - Haz clic en 'Create database'")
print("  - Elige location: southamerica-east1 (São Paulo)")
print("  - Database ID: puedes dejarlo como '(default)' o usar otro nombre")
print("  - Mode: Test mode (para desarrollo)")
print()
print("Si ya tienes la base de datos creada:")
print("  - Verifica el nombre en la parte superior de la página")
print("  - Si dice '(default)', no necesitas configurar nada")
print("  - Si tiene otro nombre, anótalo")
print()
print("=" * 60)
print()

# Preguntar al usuario
db_name = input("Ingresa el nombre de tu base de datos (deja en blanco para usar '(default)'): ").strip()

if db_name:
    print()
    print("=" * 60)
    print("CONFIGURACIÓN RECOMENDADA:")
    print("=" * 60)
    print()
    print(f"Opción 1: Editar app.py línea ~16:")
    print(f"  database_id = os.getenv('FIRESTORE_DATABASE_ID', '{db_name}')")
    print()
    print(f"Opción 2: Crear archivo .env con:")
    print(f"  FIRESTORE_DATABASE_ID={db_name}")
    print()

    # Crear archivo .env
    create_env = input("¿Quieres que cree el archivo .env automáticamente? (s/n): ").strip().lower()
    if create_env == 's':
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"# Configuración de Firestore\n")
            f.write(f"FIRESTORE_DATABASE_ID={db_name}\n")
        print()
        print("✅ Archivo .env creado exitosamente!")
        print()
        print("IMPORTANTE: Para usar variables de entorno en desarrollo, instala python-dotenv:")
        print("  pip install python-dotenv")
        print()
        print("Y agrega al inicio de app.py:")
        print("  from dotenv import load_dotenv")
        print("  load_dotenv()")
else:
    print()
    print("✅ Usarás la base de datos '(default)'. No necesitas configurar nada.")
    print()

print()
print("=" * 60)
print("PRÓXIMO PASO:")
print("=" * 60)
print("Ejecuta: python app.py")
print()

