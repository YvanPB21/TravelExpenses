# ✅ Verificación de Cambios - Guía de Pruebas

## 🧪 Cómo Verificar que Todo Funciona

### 1. Iniciar la Aplicación

```bash
python app.py
```

Deberías ver:
```
Starting Flask server on http://0.0.0.0:8000 (debug=False)
🔥 Firestore Store inicializado
```

### 2. Abrir en el Navegador

Navega a: `http://localhost:8000`

### 3. Pruebas a Realizar

#### ✅ Prueba 1: Costos Compartidos Fuera de Días

1. Crea o abre un viaje
2. Agrega algunas personas (ej: Carlos, María, Juan)
3. **Observa**: La sección "🤝 Costos Compartidos del Viaje" está DESPUÉS de las pestañas de días
4. Agrega un costo compartido (ej: "Transporte S/. 200")
5. **Verifica**: NO pide seleccionar un día
6. **Verifica**: El costo aparece en la sección general, no en ningún día específico

#### ✅ Prueba 2: Subtotales en Tabla de Items

1. Ve a cualquier día (Día 1, Día 2, etc.)
2. Agrega algunos items con diferentes precios
3. **Observa** el footer de la tabla de items
4. **Debe mostrar 3 filas**:
   ```
   Subtotal ítems: S/. XX.XX  S/. XX.XX  S/. XX.XX
   Subtotal compartido: S/. 0.00  S/. 0.00  S/. 0.00  ← Siempre 0
   Total por persona: S/. XX.XX  S/. XX.XX  S/. XX.XX
   ```

#### ✅ Prueba 3: Actualización Dinámica de Subtotales

1. En la tabla de items, **marca/desmarca** los checkboxes de personas
2. **Observa** que:
   - ✅ El "Subtotal ítems" se actualiza INMEDIATAMENTE
   - ✅ El "Total por persona" se actualiza INMEDIATAMENTE
   - ✅ El "Subtotal compartido" permanece en S/. 0.00
   - ✅ La tabla de "Resumen del Día" (debajo) se actualiza
   - ✅ El total en la pestaña del día se actualiza
   - ✅ **NO se recarga la página**

#### ✅ Prueba 4: Resumen General del Viaje

1. Desplázate hasta "📊 Resumen General del Viaje"
2. **Verifica** que muestra:
   - Total Ítems: Suma de todos los items
   - Total Compartido: Costo distribuido equitativamente
   - Total a Pagar: Ítems + Compartido
3. Al marcar/desmarcar items, estos valores se actualizan automáticamente

#### ✅ Prueba 5: Cálculo Correcto

**Escenario de prueba**:
- 3 personas: A, B, C
- Item 1: S/. 30 → Solo A y B = S/. 15 c/u
- Item 2: S/. 60 → Todos = S/. 20 c/u
- Costo compartido: S/. 90 → S/. 30 c/u

**Resultado esperado**:
- Persona A: Items S/. 35 + Compartido S/. 30 = **S/. 65**
- Persona B: Items S/. 35 + Compartido S/. 30 = **S/. 65**
- Persona C: Items S/. 20 + Compartido S/. 30 = **S/. 50**
- **Total**: S/. 180 ✓

### 4. Verificar Consola del Navegador

1. Abre las DevTools (F12)
2. Ve a la pestaña "Console"
3. Al marcar/desmarcar items, **NO debe haber errores en rojo**
4. Puede haber mensajes como: `📖 Firestore READ...` (esto es normal)

### 5. Edición de Costos Compartidos

1. Haz clic en "Editar" en un costo compartido
2. **Verifica**: NO aparece campo para "Día"
3. **Verifica**: Solo puedes editar:
   - Nombre del costo
   - Monto
   - Quién pagó (chips seleccionables)
4. Guarda y verifica que se actualiza correctamente

## 🐛 Problemas Conocidos y Soluciones

### ❌ "Subtotal compartido siempre es S/. 0.00"

✅ **Esto es CORRECTO**: Los costos compartidos son generales del viaje, no por día.
- Aparecen solo en el "Resumen General del Viaje"
- Cada día muestra solo sus items

### ❌ "Los subtotales no se actualizan"

1. Verifica que tienes conexión a internet (para Firestore)
2. Abre la consola del navegador (F12) y busca errores
3. Recarga la página completamente (Ctrl + F5)
4. Verifica que el archivo `trip_detail.html` tiene los atributos `data-*` en las celdas

### ❌ "Error 500 al cargar un viaje"

Verifica que:
1. Firebase está configurado correctamente
2. El archivo `firebase-credentials.json` existe
3. Firestore tiene la base de datos configurada

## 📊 Checklist de Verificación

Marca cada item cuando lo verifiques:

- [ ] La aplicación inicia sin errores
- [ ] Los costos compartidos están en su propia sección
- [ ] NO pide día al agregar costo compartido
- [ ] Los subtotales aparecen en el footer de la tabla
- [ ] Subtotal compartido es S/. 0.00 en días
- [ ] Los subtotales se actualizan al marcar/desmarcar
- [ ] NO se recarga la página al actualizar
- [ ] El resumen general muestra costos compartidos correctamente
- [ ] Los cálculos son correctos
- [ ] No hay errores en la consola del navegador

## 🎉 Si Todo Funciona

¡Felicidades! Los cambios están funcionando correctamente:

✅ Costos compartidos son generales del viaje
✅ Subtotales se actualizan dinámicamente
✅ Todo funciona sin recargar la página
✅ Los cálculos son precisos

## 📞 Soporte

Si encuentras algún problema:

1. Revisa los archivos de documentación:
   - `COSTOS_COMPARTIDOS_GENERALES.md`
   - `CORRECCION_SUBTOTALES.md`
   - `RESUMEN_CAMBIOS_COMPLETO.md`

2. Verifica que todos los archivos Python están actualizados:
   ```bash
   python -m py_compile models.py calculator.py app.py
   ```

3. Revisa los logs de Firestore en Firebase Console

---

**Última actualización**: 4 de Diciembre de 2025

