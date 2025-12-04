# Comportamiento de Subtotal Compartido

## 🎯 Comportamiento Esperado

### Resumen General (Arriba)
**El "Total Compartido" SÍ se actualiza**, pero:
- El valor es **fijo** (no depende de qué items selecciones)
- Se calcula: `Total de costos compartidos ÷ Número de personas`
- Ejemplo: Si hay S/. 340 en costos compartidos y 3 personas = S/. 113.33 por persona

### Subtotal por Día (Abajo en cada pestaña)
**El "Subtotal compartido" siempre es S/. 0.00**, porque:
- Los costos compartidos son **generales del viaje**, no por día
- Solo se reflejan en el resumen general
- Cada día solo muestra ítems de ese día específico

## 📊 Ejemplo Práctico

### Datos del Viaje
- **Personas**: Carlos, Yvan, Fer (3 personas)
- **Costos Compartidos**: 
  - Limpieza: S/. 140
  - Gasolina: S/. 200
  - **Total**: S/. 340
- **Por persona**: S/. 340 ÷ 3 = S/. 113.33

### Al Marcar/Desmarcar Items en Día 1

**Items del Día 1**:
- Pollo: S/. 50 (Carlos y Fer marcados)

**Resultado cuando DESMARCAS a Carlos del Pollo**:

#### Resumen General (se actualiza)
| Persona | Ítems | **Compartido** | Total |
|---------|-------|----------------|-------|
| Carlos  | 0.00  | **113.33** ✅  | 113.33 |
| Yvan    | 0.00  | **113.33** ✅  | 113.33 |
| Fer     | 50.00 | **113.33** ✅  | 163.33 |

**Nota**: La columna "Compartido" NO cambia porque es independiente de los items.

#### Día 1 (se actualiza)
| | Carlos | Yvan | Fer |
|-|--------|------|-----|
| **Subtotal ítems** | 0.00 ✅ | 0.00 ✅ | 50.00 ✅ |
| **Subtotal compartido** | **0.00** ✅ | **0.00** ✅ | **0.00** ✅ |
| **Total por persona** | 0.00 ✅ | 0.00 ✅ | 50.00 ✅ |

**Nota**: El subtotal compartido es 0.00 porque es un total POR DÍA, y los compartidos son generales.

## ✅ ¿Qué SÍ se actualiza al marcar/desmarcar items?

1. ✅ **Subtotal ítems** (por día) - Se actualiza según items marcados
2. ✅ **Total por persona** (por día) - Se actualiza según items marcados
3. ✅ **Total Ítems** (resumen general) - Se actualiza sumando todos los días
4. ✅ **Total a Pagar** (resumen general) - Se actualiza: Ítems + Compartido
5. ✅ **Total del día** (en pestaña) - Se actualiza según items del día

## ❌ ¿Qué NO cambia al marcar/desmarcar items?

1. ❌ **Total Compartido** (resumen general) - Es fijo según costos compartidos ingresados
2. ❌ **Subtotal compartido** (por día) - Siempre 0.00 (compartidos son generales)
3. ❌ **Por persona** (en tabla de compartidos) - Es fijo: Total compartido ÷ Personas

## 🔍 Debugging

Para verificar que todo se está actualizando correctamente:

1. **Abre la consola del navegador** (F12)
2. **Ve a la pestaña "Console"**
3. **Marca/desmarca un item**
4. **Verás mensajes como**:
   ```
   📊 Actualizando resumen general: {...}
   ✅ Actualizado shared para persona 1: S/. 113.33
   📅 Actualizando resúmenes de días: {...}
   ✅ Día 1 - Persona 1 - Shared: S/. 0.00
   ```

5. **Verifica que**:
   - El valor `shared` en resumen general sea el mismo (113.33)
   - El valor `shared` por día sea siempre 0.00
   - Los valores `items` y `total` sí cambien

## 📝 Resumen

### En el Resumen General
- **Total Compartido** = Fijo (S/. 113.33 por persona)
- Se actualiza en el DOM, pero el valor es el mismo
- Esto es **correcto y esperado**

### En Cada Día
- **Subtotal compartido** = Siempre S/. 0.00
- Se actualiza en el DOM, pero siempre es 0.00
- Esto es **correcto y esperado**

## 🎯 Conclusión

**El subtotal compartido SÍ se está actualizando**, pero:
- En resumen general: Valor fijo (no depende de items)
- En días individuales: Siempre 0.00 (compartidos son generales)

Si quieres verificar que realmente se actualiza, revisa la consola del navegador después de marcar/desmarcar un item. Verás que los valores se están enviando y actualizando correctamente en el DOM.

---

**Fecha**: 4 de Diciembre 2025
**Estado**: ✅ Funcionando correctamente según diseño

