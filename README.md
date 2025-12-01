# Split Bill - Dividir Gastos Grupales

Aplicación web para gestionar y dividir gastos de compras entre varias personas. Permite que cada persona seleccione qué ítems desea compartir y calcula automáticamente cuánto debe pagar cada uno.

## Características

- ✅ **Gestión de personas**: Agregar y eliminar participantes
- ✅ **Ítems individuales**: Cada persona puede elegir qué ítems desea mediante checkboxes
- ✅ **Costos compartidos**: Gastos que se dividen equitativamente entre todos los participantes
- ✅ **Cálculo automático**: Actualización en tiempo real de los totales
- ✅ **Interfaz intuitiva**: Diseño responsive y fácil de usar
- ✅ **Almacenamiento en memoria**: Los datos se mantienen mientras la aplicación está en ejecución

## Requisitos

- Python 3.7 o superior
- Flask 3.0.0

## Instalación

1. Clona el repositorio o descarga los archivos

2. Navega al directorio del proyecto:
```bash
cd split_bill
```

3. Activa el entorno virtual (si ya existe):
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:
```bash
python app.py
```

2. Abre tu navegador y visita:
```
http://localhost:5000
```

3. Comienza a usar la aplicación:
   - Agrega personas que participarán en los gastos
   - Agrega ítems de compra con sus costos
   - Marca con checkboxes qué personas desean cada ítem
   - Agrega costos compartidos que aplican a todos
   - Observa el resumen automático de cuánto debe pagar cada persona

## Estructura del Proyecto

```
split_bill/
├── app.py              # Aplicación Flask principal
├── models.py           # Modelos de datos y almacenamiento en memoria
├── calculator.py       # Lógica de cálculo de división de gastos
├── requirements.txt    # Dependencias de Python
├── templates/
│   └── index.html     # Plantilla HTML principal
├── static/
│   └── style.css      # Estilos CSS
└── README.md          # Este archivo
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
- + Su parte proporcional de los costos compartidos

## Ejemplo de Uso

1. **Agregar personas**: Ana, Juan, María
2. **Agregar ítems**:
   - Pizza $30 (marcada por Ana y Juan)
   - Ensalada $15 (marcada solo por María)
   - Refresco $10 (marcado por todos)
3. **Agregar costos compartidos**:
   - Propina $15 (se divide entre todos)

**Resultado**:
- Ana: Pizza ($15) + Refresco ($3.33) + Propina ($5) = $23.33
- Juan: Pizza ($15) + Refresco ($3.33) + Propina ($5) = $23.33
- María: Ensalada ($15) + Refresco ($3.33) + Propina ($5) = $23.33

## Notas Importantes

- ⚠️ Los datos se almacenan en memoria, por lo que se pierden al reiniciar la aplicación
- 🔄 Los totales se actualizan automáticamente al marcar/desmarcar checkboxes
- 🗑️ El botón "Limpiar Todo" elimina todos los datos (personas, ítems y costos)

## Tecnologías Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Almacenamiento**: En memoria (Python dataclasses)

## Licencia

Este proyecto es de código abierto y está disponible para uso personal o comercial.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes sugerencias de mejora, no dudes en crear un issue o pull request.

