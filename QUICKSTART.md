# Quick Start - Split Bill con Firebase

## Inicio Rápido (5 minutos)

### 1. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 2. Configurar Firebase

#### Opción A: Usar Firebase (recomendado para producción)

1. Crea un proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Habilita Firestore Database (modo test)
3. Descarga credenciales: **Configuración > Cuentas de servicio > Generar nueva clave privada**
4. Guarda el archivo como `firebase-credentials.json`
5. Configura variable de entorno:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"
```

#### Opción B: Usar JSON Local (desarrollo rápido)

Modifica `app.py` línea 12:
```python
data_store = DataStore(use_firestore=False)
```

### 3. Ejecutar

```powershell
python app.py
```

### 4. Abrir en el navegador

```
http://localhost:5000
```

## Primeros Pasos

### Crear tu primer viaje

1. En la página principal, haz clic en "Nuevo Viaje"
2. Nombre: "Viaje a la playa"
3. Días: 3
4. Haz clic en "Crear Viaje"

### Agregar personas

1. En el viaje, agrega participantes:
   - Juan
   - María
   - Pedro

### Agregar gastos

**Items individuales:**
- Carne: $400 (compartido por Juan y María)
- Pollo: $230 (solo Pedro)
- Pan: $33 (todos)

**Costos compartidos:**
- Limpieza: $120 (se divide entre todos)

### Ver resumen

La aplicación calculará automáticamente cuánto debe pagar cada persona.

## Comandos Útiles

```powershell
# Verificar conexión a Firebase
python -c "from db.firebase_client import get_firestore_client; get_firestore_client(); print('OK')"

# Ejecutar con JSON local
# Edita app.py: data_store = DataStore(use_firestore=False)
python app.py

# Ver ayuda de migración (si tienes datos en JSON)
python scripts/migrate_to_firestore.py --help
```

## Solución de Problemas

### "Module 'firebase_admin' not found"
```powershell
pip install firebase-admin
```

### "Could not determine credentials"
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"
```

### Los datos no se guardan
- Verifica que `use_firestore=True` en `app.py` (línea 12)
- Comprueba que las credenciales estén configuradas
- Revisa las reglas de Firestore (deben permitir lectura/escritura en modo test)

## Más Información

- [Configuración completa de Firebase](FIREBASE_SETUP.md)
- [README principal](README.md)

