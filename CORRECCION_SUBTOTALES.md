# Corrección: Actualización de Subtotales

## Problemas Identificados

1. ❌ **Subtotales no se actualizaban**: Al hacer clic en los checkboxes de items, los subtotales del footer de la tabla no se actualizaban dinámicamente
2. ❌ **Subtotal compartido mostraba 0**: Como los costos compartidos ahora son generales del viaje (no por día), el subtotal compartido siempre será 0 en los días individuales

## Soluciones Implementadas

### 1. Agregado de Atributos Data a las Celdas de Subtotales

Se añadieron atributos `data-*` a cada celda del footer para facilitar su identificación:

```html
<td class="items-subtotal-value" 
    data-day="{{ day_data.day_number }}" 
    data-person="{{ person.id }}" 
    data-type="items">
    S/. {{ "%.2f"|format(day_data.day_totals[person.id].items_total) }}
</td>
```

**Atributos**:
- `data-day`: Número del día
- `data-person`: ID de la persona
- `data-type`: Tipo de subtotal (`items`, `shared`, `total`)

### 2. Actualización de la Función JavaScript `updateDaysSummaries`

La función ahora:

✅ **Actualiza los subtotales del footer** usando los atributos `data-*`:
```javascript
const itemsCell = dayContent.querySelector(
    `td[data-day="${day}"][data-person="${personId}"][data-type="items"]`
);
if (itemsCell) itemsCell.textContent = `S/. ${amounts.items_total.toFixed(2)}`;
```

✅ **Actualiza la tabla de resumen del día** (tabla separada debajo de los items)

✅ **Actualiza el total del día** en la pestaña y en el footer

### 3. Corrección del Formato de Moneda

Se corrigió el símbolo de moneda en todas las actualizaciones JavaScript:
- ❌ Antes: `$${value.toFixed(2)}`
- ✅ Ahora: `S/. ${value.toFixed(2)}`

Esto afecta a:
- `updateGeneralSummary()`: Resumen general del viaje
- `updateDaysSummaries()`: Resúmenes por día

## Comportamiento Actual

### Subtotales en la Tabla de Items

Ahora se muestran **3 filas de subtotales** al final de cada tabla de items:

1. **Subtotal ítems**: Suma de items del día para cada persona
   - ✅ Se actualiza dinámicamente al marcar/desmarcar checkboxes
   
2. **Subtotal compartido**: Siempre S/. 0.00 en días individuales
   - ℹ️ Los costos compartidos son generales del viaje
   - ℹ️ Se reflejan solo en el "Resumen General del Viaje"
   
3. **Total por persona**: Igual que subtotal ítems (ya que compartido es 0)
   - ✅ Se actualiza dinámicamente al marcar/desmarcar checkboxes

### ¿Por Qué el Subtotal Compartido es 0?

Los **costos compartidos** ahora son **generales del viaje**, no están asociados a días específicos:

- **En días individuales**: Solo se muestran los gastos de ítems del día
- **En el resumen general**: Se incluyen los costos compartidos distribuidos equitativamente

**Ejemplo**:
- Día 1: Items = S/. 50 por persona → Subtotal compartido = S/. 0
- Día 2: Items = S/. 30 por persona → Subtotal compartido = S/. 0
- **Resumen General**: Items = S/. 80, Compartido = S/. 25 → **Total = S/. 105**

## Archivos Modificados

### `templates/trip_detail.html`

1. **Líneas ~185-205**: Agregado atributos `data-*` a celdas de subtotales
2. **Líneas ~570-590**: Actualizado `updateGeneralSummary()` con S/.
3. **Líneas ~615-660**: Mejorado `updateDaysSummaries()` para actualizar subtotales

## Fecha de Corrección

4 de Diciembre de 2025

