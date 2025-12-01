# 🚀 COMANDOS RÁPIDOS PARA DEPLOY EN RENDER

## Ejecuta estos comandos en orden:

### 1. Preparar Credenciales
```powershell
python render_config_helper.py
```
→ Guarda el output para el PASO 5

### 2. Subir a GitHub (Primera vez)
```powershell
git init
git add .
git commit -m "Initial commit - Split Bill app"
git remote add origin https://github.com/TU_USUARIO/split-bill.git
git branch -M main
git push -u origin main
```

### 2B. Subir a GitHub (Si ya tienes Git)
```powershell
git add .
git commit -m "Preparar deploy en Render"
git push
```

### 3. Crear Cuenta en Render
→ https://render.com/ → Sign up with GitHub

### 4. Crear Web Service
→ New + → Web Service → Selecciona "split-bill" → Free plan

**Configuración:**
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`

### 5. Variables de Entorno (del helper)
```
FIREBASE_CREDENTIALS = [JSON completo del helper]
FIRESTORE_ENABLE_CACHE = true
FIRESTORE_CACHE_TTL = 5
```

### 6. Verificar
→ Espera "Live" → Abre URL → Prueba crear viaje

---

## Actualizaciones Futuras
```powershell
git add .
git commit -m "Mi cambio"
git push
```
→ Render redespliega automáticamente

---

## Troubleshooting Rápido

### Error de credenciales:
```powershell
python render_config_helper.py
# Copia JSON de nuevo en Render Environment
```

### Logs:
→ Render → Logs tab → Busca "🔥 Firebase inicializado"

### App se duerme:
→ Normal en plan free (primer request tarda 30s)
→ Usa uptimerobot.com (gratis) para mantenerla despierta

---

## URLs Importantes

- **Render Dashboard:** https://dashboard.render.com/
- **GitHub:** https://github.com/
- **Firebase Console:** https://console.firebase.google.com/
- **UptimeRobot:** https://uptimerobot.com/ (opcional)

---

## ✅ Checklist

- [ ] Ejecuté `render_config_helper.py`
- [ ] Subí código a GitHub
- [ ] Creé Web Service en Render
- [ ] Agregué FIREBASE_CREDENTIALS
- [ ] Deploy completó (Live)
- [ ] Probé la URL - funciona
- [ ] Verifiqué logs - sin errores

**¡Listo! Tu app está en producción.** 🎉

