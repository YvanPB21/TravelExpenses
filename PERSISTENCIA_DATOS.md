# ✅ PERSISTENCIA DE DATOS IMPLEMENTADA

## 🎯 FUNCIONALIDAD NUEVA

Ahora todos tus datos se **guardan automáticamente** en un archivo JSON y se **cargan al iniciar** el servidor.

---

## 📁 ARCHIVO DE DATOS

**Ubicación:** `C:\dev\split_bill\split_bill_data.json`

Este archivo almacena:
- ✅ Todos los viajes creados
- ✅ Todas las personas de cada viaje
- ✅ Todos los ítems con sus participantes
- ✅ Todos los costos compartidos
- ✅ Configuración interna (IDs, contadores, etc.)

---

## 🔄 CÓMO FUNCIONA

### **Al Iniciar el Servidor:**
1. Busca el archivo `split_bill_data.json`
2. Si existe → Carga todos los datos
3. Si no existe → Inicia vacío
4. Mensaje en consola: `✓ Datos cargados desde split_bill_data.json (X viajes)`

### **Al Hacer Cambios:**
Cada vez que realizas una acción, se guarda automáticamente:
- ✅ Crear viaje → **Guarda**
- ✅ Eliminar viaje → **Guarda**
- ✅ Agregar persona → **Guarda**
- ✅ Eliminar persona → **Guarda**
- ✅ Agregar ítem → **Guarda**
- ✅ Eliminar ítem → **Guarda**
- ✅ Marcar/desmarcar checkbox → **Guarda**
- ✅ Agregar costo compartido → **Guarda**
- ✅ Eliminar costo compartido → **Guarda**
- ✅ Limpiar todo → **Guarda**

**Mensaje en consola:** `✓ Datos guardados en split_bill_data.json`

---

## 📊 ESTRUCTURA DEL ARCHIVO JSON

```json
{
  "trips": [
    {
      "id": 1,
      "name": "Viaje a la Playa 2025",
      "description": "Fin de semana con amigos",
      "days": 3,
      "created_at": "2025-12-01T10:30:00"
    }
  ],
  "current_trip_id": 1,
  "trip_data": {
    "1": {
      "persons": [
        {"id": 1, "name": "Ana"},
        {"id": 2, "name": "Juan"}
      ],
      "items": [
        {
          "id": 1,
          "name": "Gasolina",
          "quantity": 1,
          "unit_price": 40.0,
          "day": 1,
          "url": "",
          "person_ids": [1, 2]
        }
      ],
      "shared_costs": [
        {
          "id": 1,
          "name": "Hotel",
          "cost": 150.0,
          "day": 1
        }
      ]
    }
  },
  "_next_trip_id": 2,
  "_next_person_id": {"1": 3},
  "_next_item_id": {"1": 2},
  "_next_shared_cost_id": {"1": 2}
}
```

---

## ✨ VENTAJAS

### 1. **Persistencia Total**
- Cierra el navegador → Datos guardados ✅
- Cierra el servidor → Datos guardados ✅
- Reinicia el servidor → Datos cargados automáticamente ✅
- Reinicia la PC → Datos conservados ✅

### 2. **Sin Base de Datos**
- No necesitas instalar MySQL, PostgreSQL, etc.
- Archivo de texto plano JSON
- Fácil de leer y editar manualmente si es necesario
- Fácil de respaldar (copia el archivo)

### 3. **Automático**
- No tienes que hacer nada
- Todo se guarda automáticamente
- Todo se carga automáticamente

---

## 🔧 CASOS DE USO

### **Caso 1: Trabajo Normal**
```
1. Abres http://localhost:5000
2. Creas un viaje "Vacaciones"
3. Agregas personas y gastos
4. Cierras el navegador
5. Al día siguiente...
6. Abres http://localhost:5000
7. ✅ TODO SIGUE AHÍ
```

### **Caso 2: Reinicio del Servidor**
```
1. Servidor corriendo con datos
2. Detienes el servidor (Ctrl+C)
3. Reinicias el servidor (python app.py)
4. ✅ Todos los datos se cargan automáticamente
```

### **Caso 3: Respaldo de Datos**
```
1. Copia split_bill_data.json
2. Guárdalo en otro lugar
3. Si pierdes datos, solo copia el archivo de vuelta
4. ✅ Datos restaurados
```

---

## 📝 GESTIÓN MANUAL

### **Ver los datos:**
```powershell
Get-Content C:\dev\split_bill\split_bill_data.json
```

### **Hacer respaldo:**
```powershell
Copy-Item C:\dev\split_bill\split_bill_data.json C:\dev\split_bill\backup_$(Get-Date -Format 'yyyy-MM-dd').json
```

### **Eliminar todos los datos:**
```powershell
Remove-Item C:\dev\split_bill\split_bill_data.json
# Al reiniciar el servidor, comenzará vacío
```

### **Restaurar respaldo:**
```powershell
Copy-Item C:\dev\split_bill\backup_2025-12-01.json C:\dev\split_bill\split_bill_data.json
# Reinicia el servidor
```

---

## 🎯 CÓDIGO IMPLEMENTADO

### **En `models.py`:**

1. **`__init__()`** - Carga datos al iniciar
2. **`save_to_file()`** - Guarda en JSON
3. **`load_from_file()`** - Carga desde JSON
4. **Métodos auxiliares:**
   - `_trip_to_dict()` / `_dict_to_trip()`
   - `_person_to_dict()` / `_dict_to_person()`
   - `_item_to_dict()` / `_dict_to_item()`
   - `_shared_cost_to_dict()` / `_dict_to_shared_cost()`

5. **Guardado automático** en:
   - `add_trip()`
   - `remove_trip()`
   - `add_person()`
   - `remove_person()`
   - `add_item()`
   - `remove_item()`
   - `toggle_person_for_item()`
   - `add_shared_cost()`
   - `remove_shared_cost()`
   - `clear_all()`

---

## ⚠️ IMPORTANTE

### **Datos en Memoria + Archivo**
- Los datos siguen en memoria mientras el servidor corre
- Se guardan al archivo en cada cambio
- Se cargan del archivo al iniciar

### **No es una Base de Datos Real**
- Para uso personal o grupos pequeños: ✅ Perfecto
- Para producción con muchos usuarios: ❌ Usar DB real (PostgreSQL, MySQL)

### **Concurrencia**
- Si dos personas usan el sistema al mismo tiempo, el último guardado gana
- Para un solo grupo/equipo: No hay problema
- Para múltiples grupos simultáneos: Considerar base de datos

---

## 🚀 PROBAR AHORA

1. **Inicia el servidor:**
   ```
   python app.py
   ```

2. **Verás el mensaje:**
   ```
   No existe archivo de datos. Iniciando con datos vacíos.
   ```
   O:
   ```
   ✓ Datos cargados desde split_bill_data.json (X viajes)
   ```

3. **Crea un viaje y agrega datos**

4. **Detén el servidor** (Ctrl+C)

5. **Verifica que existe el archivo:**
   ```powershell
   Get-Item C:\dev\split_bill\split_bill_data.json
   ```

6. **Reinicia el servidor:**
   ```
   python app.py
   ```

7. **Verás:**
   ```
   ✓ Datos cargados desde split_bill_data.json (1 viajes)
   ```

8. **Abre el navegador:**
   ```
   http://localhost:5000
   ```

9. **✅ Todos tus datos siguen ahí!**

---

## 📋 RESUMEN

| Característica | Estado |
|----------------|--------|
| Persistencia automática | ✅ |
| Guardado en cada acción | ✅ |
| Carga al iniciar | ✅ |
| Formato JSON legible | ✅ |
| Sin dependencias externas | ✅ |
| Fácil respaldo | ✅ |
| Restauración simple | ✅ |

---

## 🎉 ¡YA ESTÁ FUNCIONANDO!

Tus datos ahora **se guardan automáticamente** y **persisten** entre sesiones del servidor.

**No tienes que hacer nada especial, todo funciona automáticamente.** ✨

---

*Implementado: 2025-12-01*
*Archivo: split_bill_data.json*
*Estado: ✅ ACTIVO*

