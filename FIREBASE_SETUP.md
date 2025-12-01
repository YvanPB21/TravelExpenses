# Configuración de Firebase para Split Bill

Esta guía explica cómo configurar Firebase Firestore para que la aplicación funcione con la base de datos en la nube de forma gratuita.

## 1. Crear Proyecto en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Haz clic en "Agregar proyecto" o "Add project"
3. Nombre del proyecto: `split-bill` (o el que prefieras)
4. Desactiva Google Analytics (no es necesario para este proyecto)
5. Haz clic en "Crear proyecto"

## 2. Configurar Firestore Database

1. En el menú lateral, ve a **Build > Firestore Database**
2. Haz clic en "Crear base de datos" o "Create database"
3. Selecciona modo de prueba:
   - **Modo de prueba (Test mode)**: permite lectura/escritura por 30 días (para desarrollo)
   - Ubicación: selecciona la más cercana (ej: `southamerica-east1` para Brasil)
4. Haz clic en "Habilitar" o "Enable"

## 3. Obtener Credenciales

### Opción A: Para desarrollo local (Service Account)

1. Ve a **Configuración del proyecto** (ícono de engranaje) > **Cuentas de servicio**
2. Haz clic en "Generar nueva clave privada"
3. Se descargará un archivo JSON (ej: `split-bill-xxxxx-firebase-adminsdk.json`)
4. **IMPORTANTE**: Guarda este archivo en un lugar seguro y NO lo subas a Git
5. Mueve el archivo a tu proyecto:
   ```powershell
   Move-Item "C:\Users\TuUsuario\Downloads\split-bill-xxxxx.json" "C:\dev\split_bill\firebase-credentials.json"
   ```
6. Configura la variable de entorno:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"
   ```

### Opción B: Para despliegue en la nube

Para desplegar en Firebase Hosting o Cloud Run, no necesitas credenciales explícitas, ya que usarán Application Default Credentials automáticamente.

## 4. Actualizar .gitignore

Asegúrate de que tu `.gitignore` incluya:

```
# Firebase credentials
firebase-credentials.json
*-firebase-adminsdk-*.json

# Environment variables
.env
.env.local
```

## 5. Configurar Reglas de Seguridad

En la consola de Firebase, ve a **Firestore Database > Reglas** y configura:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permitir lectura/escritura (solo para desarrollo)
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**⚠️ IMPORTANTE**: Estas reglas son solo para desarrollo. Para producción, debes implementar autenticación y reglas más restrictivas.

## 6. Instalar Dependencias

```powershell
pip install firebase-admin
```

## 7. Ejecutar la Aplicación

### Modo Firestore (por defecto):

```powershell
# Configurar credenciales
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"

# Ejecutar
python app.py
```

### Modo JSON local (legacy):

Si quieres seguir usando JSON local en lugar de Firebase:

```python
# En app.py, modifica la línea:
data_store = DataStore(use_firestore=False)
```

## 8. Verificar Configuración

Ejecuta este comando para verificar que Firebase está configurado correctamente:

```powershell
python -c "from db.firebase_client import get_firestore_client; client = get_firestore_client(); print('✓ Firebase conectado correctamente')"
```

## 9. Estructura de Datos en Firestore

La aplicación crea las siguientes colecciones:

- **trips**: Información de viajes
  - Documento: `{trip_id}`
  - Campos: `id, name, description, days, created_at`

- **persons**: Personas en cada viaje
  - Documento: `{trip_id}_{person_id}`
  - Campos: `trip_id, id, name`

- **items**: Items de compra
  - Documento: `{trip_id}_{item_id}`
  - Campos: `trip_id, id, name, quantity, unit_price, day, url, person_ids[], paid_by_person_id`

- **shared_costs**: Costos compartidos
  - Documento: `{trip_id}_{shared_cost_id}`
  - Campos: `trip_id, id, name, cost, day`

- **metadata**: Contadores y datos del sistema
  - `global_counters`: Contadores globales
  - `counters_trip_{trip_id}`: Contadores por viaje
  - `current_trip`: ID del viaje actual

## 10. Límites del Plan Gratuito (Spark)

- **Almacenamiento**: 1 GB
- **Lecturas**: 50,000 por día
- **Escrituras**: 20,000 por día
- **Eliminaciones**: 20,000 por día

Para una app personal o de equipo pequeño, estos límites son más que suficientes.

## 11. Despliegue Gratuito

### Opción 1: Firebase Hosting + Cloud Functions
- Hosting estático gratuito
- 125,000 invocaciones de funciones/mes gratis

### Opción 2: Render.com
- Plan gratuito con 750 horas/mes
- Se suspende tras 15 min de inactividad

### Opción 3: Railway.app
- $5 de crédito mensual gratis
- Paga por uso

## Solución de Problemas

### Error: "Could not automatically determine credentials"

```powershell
# Configura la variable de entorno
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"
```

### Error: "Permission denied"

- Verifica que las reglas de Firestore permitan lectura/escritura
- Revisa que el archivo de credenciales tenga los permisos correctos

### Error: "Module not found: firebase_admin"

```powershell
pip install firebase-admin
```

## Próximos Pasos

1. ✅ Configurar Firebase
2. ✅ Probar localmente
3. 📝 Implementar autenticación de usuarios
4. 🚀 Desplegar en Firebase Hosting o Render
5. 🔒 Configurar reglas de seguridad para producción

