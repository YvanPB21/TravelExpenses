"""Script para facilitar la configuración de Firebase en Render."""
import json
import os
import sys

print("=" * 70)
print("HELPER PARA CONFIGURAR FIREBASE EN RENDER")
print("=" * 70)

# Buscar archivo de credenciales
cred_files = [
    'firebase-credentials.json',
    'serviceAccountKey.json',
]

cred_path = None
for file in cred_files:
    if os.path.exists(file):
        cred_path = file
        break

if not cred_path:
    print("\n❌ No se encontró archivo de credenciales de Firebase")
    print("\nBusqué estos archivos:")
    for file in cred_files:
        print(f"  - {file}")
    print("\n💡 Descarga las credenciales desde Firebase Console:")
    print("   1. Ve a Firebase Console > Configuración > Cuentas de servicio")
    print("   2. Haz clic en 'Generar nueva clave privada'")
    print("   3. Guarda el archivo como 'firebase-credentials.json'")
    sys.exit(1)

print(f"\n✅ Encontrado: {cred_path}")

# Leer credenciales
try:
    with open(cred_path, 'r', encoding='utf-8') as f:
        creds = json.load(f)
    print("✅ Credenciales válidas")
except Exception as e:
    print(f"\n❌ Error al leer credenciales: {e}")
    sys.exit(1)

# Mostrar información del proyecto
print(f"\n📋 Información del proyecto:")
print(f"   Project ID: {creds.get('project_id', 'N/A')}")
print(f"   Client Email: {creds.get('client_email', 'N/A')}")

print("\n" + "=" * 70)
print("OPCIONES PARA CONFIGURAR EN RENDER")
print("=" * 70)

print("\n📌 OPCIÓN 1: Variable de Entorno FIREBASE_CREDENTIALS (Más Fácil)")
print("-" * 70)
print("\nEn Render, ve a: Environment → Add Environment Variable")
print("\nKey:")
print("FIREBASE_CREDENTIALS")
print("\nValue (copia todo esto):")
print("-" * 70)
creds_json = json.dumps(creds)
print(creds_json)
print("-" * 70)

print("\n📌 OPCIÓN 2: Secret File (Más Seguro)")
print("-" * 70)
print("\nEn Render, ve a: Environment → Secret Files → Add Secret File")
print("\nFilename:")
print("/etc/secrets/firebase-credentials.json")
print("\nContents (copia todo esto):")
print("-" * 70)
with open(cred_path, 'r', encoding='utf-8') as f:
    print(f.read())
print("-" * 70)

print("\nLuego agrega esta variable de entorno:")
print("Key: GOOGLE_APPLICATION_CREDENTIALS")
print("Value: /etc/secrets/firebase-credentials.json")

print("\n" + "=" * 70)
print("VARIABLES DE ENTORNO ADICIONALES (RECOMENDADAS)")
print("=" * 70)

additional_vars = {
    'FIRESTORE_ENABLE_CACHE': 'true',
    'FIRESTORE_CACHE_TTL': '5',
    'DEBUG_FIRESTORE': 'false'
}

for key, value in additional_vars.items():
    print(f"\nKey: {key}")
    print(f"Value: {value}")

print("\n" + "=" * 70)
print("SIGUIENTES PASOS")
print("=" * 70)

print("\n1. Ve a tu servicio en Render")
print("2. Tab 'Environment'")
print("3. Agrega las variables usando OPCIÓN 1 o OPCIÓN 2")
print("4. Haz clic en 'Save Changes'")
print("5. El servicio se reiniciará automáticamente")
print("\n✅ ¡Listo! Tu app debería funcionar con Firebase")

print("\n💡 Para verificar que funciona:")
print("   - Ve al tab 'Logs' y busca: '🔥 Firebase inicializado'")
print("   - Abre tu URL de Render y prueba crear un viaje")

print("\n" + "=" * 70)

