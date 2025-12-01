# 🚀 Inicio Rápido - Split Bill

## Para ejecutar la aplicación:

1. **Activar el entorno virtual:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Ejecutar la aplicación:**
   ```powershell
   python app.py
   ```

3. **Abrir en el navegador:**
   ```
   http://localhost:5000
   ```

## Estructura de Archivos Creados:

```
split_bill/
├── app.py              # 🎯 Aplicación Flask principal (EJECUTAR ESTE)
├── models.py           # 📦 Modelos de datos
├── calculator.py       # 🧮 Lógica de cálculo
├── requirements.txt    # 📋 Dependencias
├── test.py            # ✅ Script de prueba
├── README.md          # 📖 Documentación completa
├── .gitignore         # 🚫 Archivos a ignorar en git
├── templates/
│   └── index.html     # 🎨 Interfaz HTML
└── static/
    └── style.css      # 💅 Estilos CSS
```

## Funcionalidades Implementadas:

✅ **Gestión de Personas**
   - Agregar/eliminar personas del grupo

✅ **Ítems de Compra**
   - Agregar ítems con costo
   - Seleccionar qué personas participan (checkboxes)
   - El costo se divide solo entre los seleccionados

✅ **Costos Compartidos**
   - Gastos que se dividen entre TODOS (propina, delivery, etc.)

✅ **Cálculo Automático**
   - Actualización en tiempo real al marcar/desmarcar
   - Resumen detallado por persona
   - Total general

✅ **Interfaz Moderna**
   - Diseño responsive
   - Colores diferenciados
   - Fácil de usar

## Comandos Útiles:

### Instalar dependencias (si es necesario):
```powershell
pip install -r requirements.txt
```

### Ejecutar pruebas:
```powershell
python test.py
```

### Detener el servidor:
Presiona `Ctrl + C` en la terminal donde está corriendo

---

## 🎉 ¡Todo listo para usar!

La aplicación está completamente funcional y lista para gestionar gastos grupales.

