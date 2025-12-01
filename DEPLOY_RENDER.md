# 🚀 Guía Paso a Paso para Desplegar en Render

## Preparación Completada ✅

Los siguientes archivos ya están creados y listos:
- ✅ `Procfile` - Configuración para ejecutar la app
- ✅ `render.yaml` - Configuración de Render
- ✅ `requirements.txt` - Actualizado con gunicorn
- ✅ `.gitignore` - Actualizado para no subir credenciales

---

## 📋 PASO A PASO

### PASO 1: Subir el Código a GitHub

#### Opción A: Si ya tienes Git inicializado
```powershell
# Verificar status
git status

# Agregar todos los archivos nuevos
git add .

# Commit
git commit -m "Preparar app para deploy en Render"

# Push (si ya tienes remote configurado)
git push origin main
```

#### Opción B: Si NO tienes Git inicializado
```powershell
# 1. Ir a tu carpeta del proyecto
cd C:\dev\split_bill

# 2. Inicializar Git
git init

# 3. Agregar todos los archivos
git add .

# 4. Primer commit
git commit -m "Initial commit - Split Bill app"

# 5. Crear repositorio en GitHub
# Ve a https://github.com/new
# Nombre: split-bill
# Descripción: App para dividir gastos grupales
# Público o Privado (tu elección)
# NO marques "Initialize with README"
# Clic en "Create repository"

# 6. Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/split-bill.git
git branch -M main
git push -u origin main
```

---

### PASO 2: Crear Cuenta en Render

1. Ve a https://render.com/
2. Haz clic en **"Get Started"** o **"Sign Up"**
3. Opciones de registro:
   - **Recomendado:** Sign up with GitHub (más fácil)
   - O usa tu email

4. Verifica tu email si es necesario

---

### PASO 3: Crear Web Service en Render

1. Una vez en tu dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**

3. **Conectar Repositorio:**
   - Si usaste "Sign up with GitHub", verás tus repos directamente
   - Si no, haz clic en "Connect account" → GitHub
   - Busca y selecciona tu repositorio **"split-bill"**

4. **Configurar el Service:**
   ```
   Name: split-bill
   Region: Oregon (US West) [o el más cercano a ti]
   Branch: main
   Root Directory: (dejar vacío)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
   ```

5. **Plan:** Selecciona **"Free"** (gratis)

6. **NO hagas clic en "Create Web Service" todavía** ⚠️

---

### PASO 4: Configurar Variables de Entorno

Antes de crear el servicio, necesitas configurar las credenciales de Firebase:

1. En la página de configuración (antes de crear), busca la sección **"Environment Variables"**

2. Haz clic en **"Add Environment Variable"**

3. NO uses variables de entorno normales para el archivo de credenciales. En su lugar:
   - Render necesita que subas el archivo JSON de credenciales como **Secret File**

---

### PASO 5: Subir Credenciales de Firebase (IMPORTANTE)

**Opción A: Usar Secret Files (Recomendado)**

1. Después de crear el Web Service (paso siguiente), ve a:
   - Dashboard → Tu servicio "split-bill" → **"Environment"** tab
   
2. En la sección **"Secret Files"**, haz clic en **"Add Secret File"**

3. Configurar:
   ```
   Filename: /etc/secrets/firebase-credentials.json
   Contents: [Pega TODO el contenido de tu archivo firebase-credentials.json]
   ```

4. Haz clic en **"Save"**

5. Ahora agrega una variable de entorno:
   ```
   Key: GOOGLE_APPLICATION_CREDENTIALS
   Value: /etc/secrets/firebase-credentials.json
   ```

**Opción B: Usar variable de entorno (Alternativa)**

Si prefieres usar variable de entorno directamente:

1. Copia TODO el contenido de tu `firebase-credentials.json`

2. Agregar variable de entorno:
   ```
   Key: FIREBASE_CREDENTIALS
   Value: [Pega todo el JSON aquí]
   ```

3. Luego necesitarás modificar `db/firebase_client.py` para leer desde la variable (te ayudo después si eliges esta opción)

---

### PASO 6: Crear el Web Service

1. Ahora SÍ, haz clic en **"Create Web Service"**

2. Render comenzará a:
   - ✅ Clonar tu repositorio
   - ✅ Instalar dependencias (pip install -r requirements.txt)
   - ✅ Iniciar tu aplicación

3. Esto tomará **2-5 minutos** en el primer deploy

4. Verás logs en tiempo real mostrando el progreso

---

### PASO 7: Configurar las Credenciales de Firebase

Una vez que el servicio esté "Live" (puede fallar primero, es normal):

1. Ve a **"Environment"** tab en tu servicio

2. Si usaste **Opción A (Secret Files)**:
   ```
   Secret Files:
   - Filename: /etc/secrets/firebase-credentials.json
   - Contents: [Tu JSON completo]
   
   Environment Variables:
   - GOOGLE_APPLICATION_CREDENTIALS = /etc/secrets/firebase-credentials.json
   - FIRESTORE_ENABLE_CACHE = true
   - FIRESTORE_CACHE_TTL = 5
   ```

3. Haz clic en **"Save Changes"**

4. El servicio se reiniciará automáticamente

---

### PASO 8: Verificar que Funciona

1. Una vez que el servicio muestre **"Live"** (círculo verde):

2. Haz clic en la URL generada (algo como: `https://split-bill-xxxx.onrender.com`)

3. Deberías ver tu aplicación funcionando! 🎉

4. Prueba:
   - Crear un viaje
   - Agregar personas
   - Agregar items
   - Verificar que se guarden en Firestore

---

### PASO 9: Configurar Dominio Personalizado (Opcional)

Si quieres usar tu propio dominio:

1. En tu servicio de Render, ve a **"Settings"**

2. En la sección **"Custom Domain"**, haz clic en **"Add Custom Domain"**

3. Ingresa tu dominio (ej: `splitbill.midominio.com`)

4. Render te dará un CNAME para configurar en tu proveedor de DNS

5. Agrega el CNAME en tu proveedor (GoDaddy, Namecheap, Cloudflare, etc.)

6. Espera 5-10 minutos para propagación DNS

7. ✅ Tu app estará en tu dominio personalizado con HTTPS gratis

---

## 🔧 Solución de Problemas

### Error: "Could not determine credentials"

**Solución:**
1. Verifica que agregaste el Secret File correctamente
2. Verifica que la variable `GOOGLE_APPLICATION_CREDENTIALS` apunta a `/etc/secrets/firebase-credentials.json`
3. Reinicia el servicio: Settings → Manual Deploy → "Clear build cache & deploy"

### Error: "Module 'gunicorn' not found"

**Solución:**
```powershell
# Localmente, regenera requirements.txt
pip freeze > requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Update requirements"
git push

# Render detectará el cambio y redesplegará automáticamente
```

### Error: "Application startup failed"

**Solución:**
1. Ve a **"Logs"** tab en Render
2. Busca el error específico
3. Errores comunes:
   - Falta firebase-credentials.json → Revisa PASO 5
   - Puerto incorrecto → Verifica que uses `$PORT` en Procfile
   - Timeout → Aumenta timeout en Procfile (ya está en 120s)

### La app se duerme después de 15 minutos

**Esto es normal en el plan gratuito:**
- Render duerme los servicios gratuitos tras 15 min de inactividad
- El primer request después tardará ~30 segundos (cold start)
- Requests subsecuentes serán normales

**Soluciones:**
1. **Upgrade a plan pago** ($7/mes - no se duerme)
2. **Usar un servicio de "keep-alive"** como UptimeRobot (gratis) que hace ping cada 5 minutos
3. **Aceptarlo** - Para apps personales está bien

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real
1. En tu servicio de Render, ve a **"Logs"** tab
2. Verás todos los logs de tu aplicación
3. Útil para debugging

### Métricas
1. **"Metrics"** tab muestra:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🔄 Actualizaciones Futuras

Cada vez que hagas cambios:

```powershell
# 1. Hacer cambios en tu código local

# 2. Commit
git add .
git commit -m "Descripción de tus cambios"

# 3. Push
git push

# 4. Render detectará automáticamente y redesplegará
# No necesitas hacer nada más!
```

---

## 🎯 Checklist Final

Antes de declarar éxito, verifica:

- [ ] Servicio muestra "Live" (círculo verde)
- [ ] URL de Render abre tu app
- [ ] Puedes crear un viaje nuevo
- [ ] Puedes agregar personas
- [ ] Puedes agregar items
- [ ] Los datos persisten (refresca la página y siguen ahí)
- [ ] No hay errores en los Logs

---

## 🆘 Si Necesitas Ayuda

Si algo no funciona:

1. **Copia el error de los Logs** (tab "Logs" en Render)
2. **Revisa los pasos anteriores**
3. **Errores comunes están en "Solución de Problemas"**

---

## 🎉 ¡Listo!

Tu aplicación ahora está desplegada en Render de forma gratuita con:

✅ HTTPS automático  
✅ Deploy automático desde GitHub  
✅ Logs y monitoreo  
✅ Firebase Firestore funcionando  
✅ Optimizaciones de rendimiento activas  

**URL de tu app:** `https://split-bill-XXXX.onrender.com`

---

## 📝 Próximos Pasos Sugeridos

1. **Compartir la URL** con tu equipo
2. **Configurar un dominio personalizado** (opcional)
3. **Configurar UptimeRobot** para evitar que se duerma (opcional)
4. **Implementar autenticación de usuarios** (Firebase Auth)
5. **Añadir PWA** para instalar como app móvil

¡Felicidades! 🚀

