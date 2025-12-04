# Costos Compartidos Generales del Viaje

## Cambios Realizados

Se modificó la aplicación para que los **costos compartidos** ya no estén asociados a días específicos, sino que sean **generales del viaje completo**.

### Modificaciones en el Modelo de Datos

#### `models.py`
- ✅ **SharedCost**: Eliminado el campo `day` del dataclass
- ✅ **Serialización**: Actualizado `_shared_cost_to_dict` y `_dict_to_shared_cost` para no incluir el campo `day`
- ✅ **Métodos**:
  - Eliminado `get_shared_costs_by_day()` - ya no es necesario filtrar por día
  - Actualizado `add_shared_cost()` - removido parámetro `day`
  - Actualizado `update_shared_cost()` - removido parámetro `day`

#### `db/firestore_store.py`
- ✅ **add_shared_cost**: Removido parámetro `day` y campo en documento Firestore
- ✅ **update_shared_cost**: Removido lógica de actualización del campo `day`
- ✅ **_doc_to_shared_cost**: Actualizado para no leer el campo `day` de Firestore
- ✅ **Métodos eliminados**: `get_shared_costs_by_day()` - ya no se filtra por día

### Modificaciones en la Calculadora

#### `calculator.py`
- ✅ **calculate_totals_by_day()**: 
  - Ya no calcula costos compartidos por día
  - Solo calcula totales de ítems para cada día
  - El campo `shared_total` queda en 0 para los totales diarios
  
- ✅ **calculate_totals()**: 
  - Los costos compartidos se calculan una sola vez para todo el viaje
  - Se distribuyen equitativamente entre todas las personas
  - Se suman al total general de cada persona
  
- ✅ **get_day_total()**: 
  - Ya no incluye costos compartidos
  - Solo suma el total de ítems del día

### Modificaciones en las Rutas

#### `app.py`
- ✅ **trip_detail**: 
  - Removida la obtención de `day_shared_costs` para cada día
  - Agregado `shared_costs` global al contexto del template
  
- ✅ **add_shared_cost**: 
  - Removido el parámetro `day` del formulario
  - Ya no se valida ni procesa el día
  
- ✅ **update_shared_cost**: 
  - Removido el parámetro `day` de la actualización

### Modificaciones en el Template

#### `templates/trip_detail.html`
- ✅ **Sección de Costos Compartidos**:
  - Movida FUERA del loop de días
  - Ahora es una sección independiente después de las pestañas de días
  - Título cambiado a "🤝 Costos Compartidos del Viaje"
  
- ✅ **Formulario de Agregar**:
  - Removido el campo hidden `day`
  - Ya no se asocia a un día específico
  
- ✅ **Formulario de Editar**:
  - Removido el input de `day`
  - Solo permite editar nombre, costo y quién pagó

## Comportamiento Actual

### Cálculo de Totales

1. **Por Día**: Los totales por día solo incluyen ítems de ese día
2. **Compartidos**: Los costos compartidos se distribuyen equitativamente entre TODAS las personas del viaje
3. **Total General**: Suma de ítems + parte proporcional de costos compartidos

### Ejemplo

**Viaje de 3 días con 4 personas**

- **Día 1**: Ítems por S/. 100
- **Día 2**: Ítems por S/. 200
- **Día 3**: Ítems por S/. 150
- **Costos Compartidos**: S/. 400 (transporte, alojamiento, etc.)

**Distribución**:
- Cada persona paga su parte de ítems según participación
- Cada persona paga S/. 100 de costos compartidos (400 ÷ 4)
- **Total por persona** = Ítems asignados + S/. 100

## Ventajas del Cambio

✅ **Simplicidad**: Los gastos compartidos (transporte, alojamiento) naturalmente son del viaje completo, no de un día específico

✅ **Menos redundancia**: No hay que repetir costos compartidos en cada día

✅ **Claridad**: Separación clara entre gastos diarios (ítems) y gastos generales (compartidos)

✅ **Facilidad de uso**: Un solo lugar para gestionar todos los costos compartidos del viaje

## Compatibilidad

⚠️ **Nota**: Los costos compartidos existentes en Firestore que tengan el campo `day` seguirán funcionando, pero el campo será ignorado. Se recomienda eliminar el campo `day` de documentos existentes en Firestore para mantener consistencia.

## Fecha de Implementación

4 de Diciembre de 2025

