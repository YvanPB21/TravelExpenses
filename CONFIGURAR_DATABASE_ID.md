# Configuración del Nombre de Base de Datos en Firestore

## Problema
Por defecto, Firestore crea una base de datos llamada `(default)`. Si has creado una base de datos con otro nombre en Firebase, necesitas especificarlo en la configuración.

## Solución

### Opción 1: Variable de Entorno (Recomendado para producción)

Crea un archivo `.env` en la raíz del proyecto:

```bash
FIRESTORE_DATABASE_ID=split-bill-db
```

O en Render/Railway/etc., agrega la variable de entorno:
- **Variable**: `FIRESTORE_DATABASE_ID`
- **Valor**: `split-bill-db` (o el nombre de tu base de datos)

### Opción 2: Modificar directamente en app.py

En `app.py`, línea ~16, cambia:

```python
database_id = os.getenv('FIRESTORE_DATABASE_ID', 'split-bill-db')
```

Reemplaza `'split-bill-db'` con el nombre de tu base de datos.

### Opción 3: No especificar (usar default)

Si tu base de datos se llama `(default)`, simplemente usa:

```python
database_id = os.getenv('FIRESTORE_DATABASE_ID', None)
```

O comenta la línea `database_id`:

```python
firebase_config = FirebaseConfig(
    credentials_path=credentials_file
    # No especificar database_id usará "(default)"
)
```

## Cómo verificar el nombre de tu base de datos

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto: `travelexpenses-301bc`
3. Ve a **Firestore Database**
4. En la parte superior verás el nombre de la base de datos

## Crear una nueva base de datos en Firestore

Si aún no has creado la base de datos:

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto: `travelexpenses-301bc`
3. Ve a **Firestore Database**
4. Haz clic en **Create database**
5. Elige:
   - **Location**: `southamerica-east1` (São Paulo) - el más cercano
   - **Database ID**: `split-bill-db` (o déjalo como `(default)`)
   - **Mode**: Production mode o Test mode (recomendado Test mode para desarrollo)

## Ejemplo completo

```python
# En app.py
firebase_config = FirebaseConfig(
    credentials_path='firebase-credentials.json',
    database_id='split-bill-db'  # Tu nombre de DB aquí
)
```

## Verificación

Después de configurar, al ejecutar `python app.py` deberías ver:

```
🔥 Firebase inicializado desde firebase-credentials.json
Starting Flask server on http://0.0.0.0:5000
```

Sin errores de "database does not exist".

