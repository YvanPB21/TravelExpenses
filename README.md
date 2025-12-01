# Split Bill - Dividir Gastos Grupales

Aplicación web para gestionar y dividir gastos de compras entre varias personas. Permite que cada persona seleccione qué ítems desea compartir y calcula automáticamente cuánto debe pagar cada uno.

## Características

- ✅ **Gestión de personas**: Agregar y eliminar participantes
- ✅ **Ítems individuales**: Cada persona puede elegir qué ítems desea mediante checkboxes
- ✅ **Costos compartidos**: Gastos que se dividen equitativamente entre todos los participantes
- ✅ **Cálculo automático**: Actualización en tiempo real de los totales
- ✅ **Interfaz intuitiva**: Diseño responsive y fácil de usar
- ✅ **Firebase Firestore**: Almacenamiento en la nube gratuito (plan Spark)
- ✅ **Múltiples viajes**: Gestiona varios viajes/eventos simultáneamente
- ✅ **Organización por días**: Divide gastos por días del viaje
- ✅ **Optimizado para rendimiento**: Caché inteligente y batch operations (~90% más rápido)

## Requisitos

- Python 3.10 o superior
- Cuenta de Firebase (gratuita)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd split_bill
```

### 2. Crear y activar entorno virtual

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar Firebase

Consulta la guía completa en [FIREBASE_SETUP.md](FIREBASE_SETUP.md) para:
- Crear proyecto en Firebase
- Configurar Firestore
- Obtener credenciales
- Configurar reglas de seguridad

**Resumen rápido:**

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto
3. Habilita Firestore Database (modo test)
4. Descarga las credenciales de la cuenta de servicio
5. Guarda el archivo como `firebase-credentials.json` en el directorio del proyecto
6. Configura la variable de entorno:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"
```

## Uso

### Ejecutar con Firebase (por defecto)

```powershell
# Configurar credenciales (si no lo hiciste antes)
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"

# Ejecutar la aplicación
python app.py
```

### Ejecutar con JSON local (modo legacy)

Si prefieres usar almacenamiento local en lugar de Firebase:

1. Modifica `app.py` línea 12:
```python
data_store = DataStore(use_firestore=False)
```

2. Ejecuta normalmente:
```powershell
python app.py
```

### Acceder a la aplicación

Abre tu navegador en:
```
http://localhost:5000
```

## Estructura del Proyecto

```
split_bill/
├── app.py                      # Aplicación Flask principal
├── models.py                   # Modelos de datos (con soporte Firestore y JSON)
├── calculator.py               # Lógica de cálculo de división de gastos
├── requirements.txt            # Dependencias de Python
├── FIREBASE_SETUP.md          # Guía de configuración de Firebase
├── db/
│   ├── firebase_client.py     # Cliente de Firebase
│   └── firestore_store.py     # Capa de acceso a Firestore
├── scripts/
│   └── migrate_to_firestore.py # Script de migración (opcional)
├── templates/
│   ├── index.html             # Lista de viajes
│   ├── trips.html             # Vista de viajes
│   └── trip_detail.html       # Detalle de un viaje
├── static/
│   └── style.css              # Estilos CSS
└── README.md                  # Este archivo
```

## Funcionamiento

### Ítems Individuales
- Cada ítem tiene un costo que se divide solo entre las personas que lo marcan
- Si un ítem cuesta $100 y 2 personas lo marcan, cada una paga $50
- Si nadie marca un ítem, no se cobra a nadie

### Costos Compartidos
- Los costos compartidos se dividen equitativamente entre TODAS las personas
- Si hay un costo compartido de $60 y 3 personas, cada una paga $20

### Cálculo Total
El total que debe pagar cada persona es:
- Suma de su parte proporcional de los ítems marcados
- \+ Su parte proporcional de los costos compartidos

## Despliegue Gratuito

### Opción 1: Firebase Hosting + Cloud Functions
- Hosting estático gratuito
- 125,000 invocaciones gratis/mes
- [Guía de despliegue](https://firebase.google.com/docs/hosting)

### Opción 2: Render.com
- Plan gratuito con 750 horas/mes
- [Render.com](https://render.com/)

### Opción 3: Railway.app
- $5 de crédito mensual gratis
- [Railway.app](https://railway.app/)

## Límites del Plan Gratuito de Firebase

- **Almacenamiento**: 1 GB
- **Lecturas**: 50,000 por día
- **Escrituras**: 20,000 por día
- **Eliminaciones**: 20,000 por día

Suficiente para equipos pequeños y uso personal.

## Rendimiento

La aplicación incluye **optimizaciones avanzadas** de Firestore:

- ✅ **Caché inteligente con TTL** - Reduce lecturas en ~90%
- ✅ **Batch operations** - Operaciones masivas ~98% más rápidas
- ✅ **Filtrado en memoria** - Navegación entre días instantánea

**Resultado**: Respuesta típica <0.5s vs 2-3s sin optimizaciones.

📖 Ver [OPTIMIZACIONES_FIRESTORE.md](OPTIMIZACIONES_FIRESTORE.md) para detalles completos.

### Probar Optimizaciones

```powershell
# Activar modo debug
$env:DEBUG_FIRESTORE="true"

# Ejecutar pruebas
python test_optimizaciones.py
```

## Tecnologías Utilizadas

- **Backend**: Python 3.10+, Flask 3.0
- **Base de Datos**: Firebase Firestore (NoSQL)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Autenticación**: Próximamente (Firebase Auth)

## Desarrollo

### Ejecutar tests

```powershell
pytest
```

### Verificar conexión a Firebase

```powershell
python -c "from db.firebase_client import get_firestore_client; client = get_firestore_client(); print('✓ Firebase conectado')"
```

## Solución de Problemas

### Error: "Could not automatically determine credentials"
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\dev\split_bill\firebase-credentials.json"
```

### Error: "Permission denied" en Firestore
- Verifica las reglas de seguridad en Firebase Console
- Asegúrate de estar en modo test (para desarrollo)

### La aplicación no guarda datos
- Verifica que `use_firestore=True` en `app.py`
- Comprueba que las credenciales estén configuradas
- Revisa los logs en la consola

## Roadmap

- [ ] Autenticación de usuarios con Firebase Auth
- [ ] Compartir viajes entre usuarios
- [ ] Exportar resumen en PDF
- [ ] Notificaciones por email
- [ ] App móvil (React Native)
- [ ] Gráficos de gastos

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes sugerencias de mejora, no dudes en crear un issue o pull request.

## Licencia

Este proyecto es de código abierto y está disponible para uso personal o comercial.

