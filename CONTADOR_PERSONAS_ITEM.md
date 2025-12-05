# Contador de Personas por Item

## 📊 Funcionalidad Implementada

Se ha agregado un **contador dinámico** al lado del nombre de cada item que muestra cuántas personas han marcado ese item.

## ✨ Características

### 1. **Visualización del Contador**

**Ubicación**: Al lado derecho del nombre del item en la tabla.

**Formato**: `(X/Y)`
- **X**: Número de personas que marcaron el item
- **Y**: Total de personas en el viaje

**Ejemplo**:
```
POLLO (2/7)
ARROZ (5/7)
GASOLINA (1/7)
```

### 2. **Diseño Visual**

**Badge Azul**:
```css
background: linear-gradient(135deg, #e3f2fd, #bbdefb);
color: #2196F3;
border: 1px solid #90caf9;
border-radius: 12px;
padding: 2px 8px;
font-size: 0.75em;
```

**Características**:
- Gradiente azul claro
- Borde azul
- Texto azul oscuro
- Bordes redondeados
- Tamaño compacto

### 3. **Tooltip Informativo**

Al pasar el mouse sobre el contador, aparece un tooltip:
```
"2 de 7 personas"
```

Proporciona información más descriptiva del contador.

### 4. **Actualización Dinámica**

El contador se actualiza **automáticamente** cuando:
- ✅ Se marca un checkbox de persona
- ✅ Se desmarca un checkbox de persona
- ✅ Sin recargar la página
- ✅ En tiempo real

**Función JavaScript**:
```javascript
function updateItemPersonCounter(itemId) {
    // Cuenta checkboxes marcados
    // Actualiza el contador visualmente
    // Actualiza el tooltip
}
```

## 🎯 Ejemplo de Uso

### Caso 1: Item sin personas
```
POLLO (0/7)
```
- Ninguna persona ha marcado este item
- Se ve claramente que falta asignar

### Caso 2: Item con algunas personas
```
ARROZ (3/7)
```
- 3 de 7 personas marcaron este item
- Fácil de identificar distribución parcial

### Caso 3: Item con todas las personas
```
GASOLINA (7/7)
```
- Todas las personas marcaron este item
- Indica que es un gasto compartido por todos

## 📱 Diseño Responsive

### Desktop (> 768px)
```css
font-size: 0.75em;
padding: 2px 8px;
margin-left: 8px;
```

### Mobile (< 768px)
```css
font-size: 0.7em;
padding: 1px 6px;
margin-left: 4px;
```

**Ajustes**:
- Texto más pequeño
- Padding reducido
- Margin menor

## 🔄 Flujo de Actualización

### 1. Usuario marca/desmarca checkbox
```
Usuario hace clic en checkbox
        ↓
togglePersonItem() se ejecuta
        ↓
Se envía petición AJAX al servidor
        ↓
Servidor actualiza datos
        ↓
updateItemPersonCounter(itemId) se ejecuta
        ↓
Se cuenta checkboxes marcados
        ↓
Se actualiza contador: (X/Y)
        ↓
Se actualiza tooltip
```

### 2. Actualización Visual
```javascript
// Contar checkboxes marcados
let checkedCount = 0;
checkboxes.forEach(checkbox => {
    if (checkbox.checked) checkedCount++;
});

// Actualizar contador
counter.textContent = `(${checkedCount}/${totalCount})`;
counter.title = `${checkedCount} de ${totalCount} personas`;
```

## 🎨 Integración Visual

### En la Tabla de Items

```
┌─────────────────────────────────────────────────────┐
│ ITEM            │ CANT │ P.UNIT │ TOTAL │ ... │     │
├─────────────────────────────────────────────────────┤
│ POLLO (2/7)     │  1   │ 50.00  │ 50.00 │ ... │ ☑☐  │
│ ARROZ (5/7)     │  2   │ 10.00  │ 20.00 │ ... │ ☑☑  │
│ GASOLINA (7/7)  │  1   │ 80.00  │ 80.00 │ ... │ ☑☑  │
└─────────────────────────────────────────────────────┘
```

### Código HTML
```html
<td class="item-name">
    POLLO
    <span class="item-person-counter" title="2 de 7 personas">
        (2/7)
    </span>
</td>
```

## 💡 Ventajas de la Funcionalidad

1. **Visibilidad Inmediata** 👀
   - Se ve de un vistazo cuántas personas participan
   - No necesitas contar checkboxes manualmente

2. **Facilita Revisión** ✅
   - Rápido identificar items sin asignar (0/7)
   - Ver items compartidos por todos (7/7)

3. **Actualización en Tiempo Real** ⚡
   - No requiere recargar la página
   - Feedback visual instantáneo

4. **Diseño Limpio** 🎨
   - Badge compacto y elegante
   - No sobrecarga la interfaz
   - Colores coherentes con el diseño

5. **Responsive** 📱
   - Se adapta a móviles
   - Tamaño optimizado para pantallas pequeñas

## 🔍 Casos de Uso

### Escenario 1: Verificar Distribución
```
Usuario: "¿Cuántas personas van a pagar el pollo?"
Contador: POLLO (3/7)
Respuesta: 3 personas
```

### Escenario 2: Items Compartidos
```
Usuario: "¿Este gasto es de todos?"
Contador: LIMPIEZA (7/7)
Respuesta: Sí, todas las personas
```

### Escenario 3: Items Sin Asignar
```
Usuario: "¿Falta asignar este item?"
Contador: PAN (0/7)
Respuesta: Sí, nadie lo ha marcado aún
```

## 📊 Indicadores Visuales

### Estados del Contador

**Ninguna persona (0/7)**:
- Color: Azul normal
- Indica: Item sin asignar
- Acción: Necesita marcar personas

**Algunas personas (3/7)**:
- Color: Azul normal
- Indica: Distribución parcial
- Acción: Verificar si está correcto

**Todas las personas (7/7)**:
- Color: Azul normal
- Indica: Item compartido por todos
- Acción: Confirmar que es correcto

## 🛠️ Implementación Técnica

### Archivos Modificados

**1. `templates/trip_detail.html`**
- HTML del contador agregado
- Función `updateItemPersonCounter()` agregada
- Llamada a la función en `togglePersonItem()`

**2. `static/style.css`**
- Estilos para `.item-person-counter`
- Estilos responsive

### Código Principal

**HTML**:
```html
<span class="item-person-counter" title="{{ item.person_ids|length }} de {{ persons|length }} personas">
    ({{ item.person_ids|length }}/{{ persons|length }})
</span>
```

**CSS**:
```css
.item-person-counter {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    color: var(--secondary-color);
    border-radius: 12px;
    padding: 2px 8px;
    font-size: 0.75em;
    font-weight: 700;
    border: 1px solid #90caf9;
}
```

**JavaScript**:
```javascript
function updateItemPersonCounter(itemId) {
    const checkboxes = document.querySelectorAll(
        `input.person-checkbox[data-item-id="${itemId}"]`
    );
    
    let checkedCount = 0;
    checkboxes.forEach(cb => {
        if (cb.checked) checkedCount++;
    });
    
    const counter = itemRow.querySelector('.item-person-counter');
    counter.textContent = `(${checkedCount}/${checkboxes.length})`;
}
```

## 🎯 Resultado Final

### Antes
```
POLLO          1    50.00   50.00   [Alayo]   -   ☑☐☐☐☐☐☐
```

### Ahora
```
POLLO (2/7)    1    50.00   50.00   [Alayo]   -   ☑☐☐☐☐☐☐
       ↑
   Contador
```

## ✅ Checklist de Implementación

- [x] HTML del contador agregado
- [x] Estilos CSS implementados
- [x] Estilos responsive agregados
- [x] Función JavaScript de actualización
- [x] Integración con togglePersonItem()
- [x] Tooltip informativo
- [x] Testing en diferentes escenarios
- [x] Compatible con todos los navegadores

## 🎉 Beneficios

1. **UX Mejorada**: Usuario ve información clave de un vistazo
2. **Menos Errores**: Fácil detectar items sin asignar
3. **Más Eficiente**: No necesita contar checkboxes manualmente
4. **Tiempo Real**: Actualización instantánea al marcar/desmarcar
5. **Diseño Coherente**: Sigue la paleta de colores de la app

---

**Fecha de Implementación**: 5 de Diciembre 2025
**Estado**: ✅ Completamente implementado y funcional
**Archivos Modificados**: 
- `templates/trip_detail.html` (HTML + JavaScript)
- `static/style.css` (Estilos + Responsive)

