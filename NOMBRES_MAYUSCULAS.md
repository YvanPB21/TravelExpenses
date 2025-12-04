# Conversión Automática a Mayúsculas

## 📝 Cambios Implementados

Se ha implementado la conversión automática a **MAYÚSCULAS** para todos los nombres ingresados en la aplicación.

## ✅ Campos Afectados

### 1. **Nombres de Viajes** 🚗
**Función**: `add_trip()`
```python
name = request.form.get('name', '').strip().upper()
```
- Al crear un viaje, el nombre se guarda en MAYÚSCULAS
- Ejemplo: "viaje a la playa" → "VIAJE A LA PLAYA"

### 2. **Nombres de Personas** 👥
**Función**: `add_person()`
```python
name = request.form.get('name', '').strip().upper()
```
- Al agregar una persona, el nombre se guarda en MAYÚSCULAS
- Ejemplo: "carlos" → "CARLOS"
- Ejemplo: "maría josé" → "MARÍA JOSÉ"

### 3. **Nombres de Items** 📦
**Función**: `add_item()`
```python
name = request.form.get('name', '').strip().upper()
```
- Al agregar un ítem de compra, el nombre se guarda en MAYÚSCULAS
- Ejemplo: "pollo" → "POLLO"
- Ejemplo: "arroz integral" → "ARROZ INTEGRAL"

**Función**: `update_item()`
```python
name = request.form.get('name', '').strip().upper()
```
- Al editar un ítem, el nombre también se convierte a MAYÚSCULAS

### 4. **Nombres de Costos Compartidos** 🤝
**Función**: `add_shared_cost()`
```python
name = request.form.get('name', '').strip().upper()
```
- Al agregar un costo compartido, el nombre se guarda en MAYÚSCULAS
- Ejemplo: "gasolina" → "GASOLINA"
- Ejemplo: "peaje cusco" → "PEAJE CUSCO"

**Función**: `update_shared_cost()`
```python
name = request.form.get('name', '').strip().upper()
```
- Al editar un costo compartido, el nombre también se convierte a MAYÚSCULAS

## 🔧 Implementación Técnica

### Método Utilizado
```python
.strip().upper()
```

1. **`.strip()`**: Elimina espacios en blanco al inicio y final
2. **`.upper()`**: Convierte todo el texto a mayúsculas

### Ubicación de los Cambios
**Archivo**: `app.py`
**Líneas modificadas**: 6 funciones

```python
# Viajes
add_trip()          # Línea ~89

# Personas
add_person()        # Línea ~113

# Items
add_item()          # Línea ~131
update_item()       # Línea ~159

# Costos Compartidos
add_shared_cost()   # Línea ~246
update_shared_cost()# Línea ~265
```

## 📊 Ejemplos de Conversión

### Antes
```
Viaje: "viaje a cusco 2024"
Persona: "juan carlos"
Item: "pan integral"
Compartido: "alquiler de casa"
```

### Ahora
```
Viaje: "VIAJE A CUSCO 2024"
Persona: "JUAN CARLOS"
Item: "PAN INTEGRAL"
Compartido: "ALQUILER DE CASA"
```

## ✨ Beneficios

1. **Consistencia Visual**: Todos los nombres se ven uniformes
2. **Mejor Legibilidad**: Más fácil de leer en tablas y reportes
3. **Estandarización**: Evita duplicados por diferencias de mayúsculas/minúsculas
4. **Profesionalismo**: Apariencia más formal y organizada

## 🎯 Campos NO Afectados

Los siguientes campos **NO** se convierten a mayúsculas:
- ❌ Descripción del viaje
- ❌ URLs de items
- ❌ Valores numéricos (precios, cantidades, etc.)

## 💡 Notas Importantes

- La conversión es **automática** al enviar el formulario
- **No requiere** cambios en los templates HTML
- Es **transparente** para el usuario
- **Conserva** acentos y caracteres especiales (ñ, á, é, etc.)

## 🔄 Compatibilidad

- ✅ Compatible con Firebase/Firestore
- ✅ Compatible con datos existentes
- ✅ No afecta la funcionalidad actual
- ✅ Funciona en todos los navegadores

## 📱 Ejemplos de Uso

### Agregar Persona
```
Input:  "maría josé gonzález"
Output: "MARÍA JOSÉ GONZÁLEZ"
```

### Agregar Item
```
Input:  "pollo a la brasa 1/4"
Output: "POLLO A LA BRASA 1/4"
```

### Agregar Costo Compartido
```
Input:  "peaje Lima - Cañete"
Output: "PEAJE LIMA - CAÑETE"
```

---

**Fecha de Implementación**: 4 de Diciembre 2025
**Estado**: ✅ Completamente implementado
**Archivos Modificados**: `app.py` (6 funciones)

