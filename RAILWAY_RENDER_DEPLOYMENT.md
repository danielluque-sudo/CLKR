# 🚂 Deploy en Railway & Render

Guía completa para deployar tu API de leyes colombianas sin límites de timeout.

---

## 🚂 RAILWAY (Recomendado - Más fácil)

Railway es perfecto para Python y **no tiene límite de timeout**.

### ✅ Ventajas de Railway:
- ✅ Sin límite de timeout (scraping largo OK)
- ✅ Deploy automático desde GitHub
- ✅ $5/mes de crédito gratis
- ✅ Configuración super simple
- ✅ CLI poderoso

---

## 📋 Método 1: Railway con GitHub (Más fácil)

### Paso 1: Crea cuenta en Railway
👉 https://railway.app/

### Paso 2: Nuevo Proyecto
1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Conecta tu cuenta de GitHub
4. Selecciona: `danielluque-sudo/CLKR`
5. Branch: `main` (o `claude/colombian-legal-scraper-2cumr`)

### Paso 3: Configurar Variables de Entorno
En el dashboard de Railway, ve a **Variables**:

```bash
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PORT=8000
```

### Paso 4: Deploy Automático
Railway detectará automáticamente que es Python y:
- ✅ Instalará dependencias
- ✅ Ejecutará el Procfile
- ✅ Asignará un dominio público

**URL final**: `https://tu-proyecto.up.railway.app`

---

## 📋 Método 2: Railway con CLI (Más control)

```bash
# 1. Instalar Railway CLI
npm i -g @railway/cli

# O con brew (Mac)
brew install railway

# 2. Login
railway login

# 3. Ir al proyecto
cd /home/user/CLKR

# 4. Inicializar
railway init

# Selecciona:
# - Create new project? → Yes
# - Project name? → colombian-legal-api

# 5. Vincular al proyecto
railway link

# 6. Agregar variables de entorno
railway variables set SUPABASE_URL=your_supabase_url_here
railway variables set SUPABASE_KEY=your_supabase_key_here
railway variables set ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 7. Deploy
railway up

# 8. Ver logs
railway logs

# 9. Abrir en navegador
railway open
```

---

## 🎨 RENDER

Render es otra excelente opción, también sin límite de timeout.

### ✅ Ventajas de Render:
- ✅ Sin límite de timeout
- ✅ Plan gratuito disponible
- ✅ Deploy automático
- ✅ SSL gratis

### ⚠️ Desventajas:
- ⚠️ Plan gratuito "duerme" después de 15min de inactividad
- ⚠️ Más lento que Railway en arranque

---

## 📋 Deploy en Render

### Paso 1: Crea cuenta
👉 https://render.com/

### Paso 2: Nuevo Web Service
1. Click en **"New +"** → **"Web Service"**
2. Conecta GitHub
3. Selecciona: `danielluque-sudo/CLKR`

### Paso 3: Configuración

```
Name: colombian-legal-api
Region: Oregon (US West)
Branch: main
Root Directory: (dejar vacío)
Runtime: Python 3
Build Command: pip install -r requirements-deploy.txt
Start Command: uvicorn api.app:app --host 0.0.0.0 --port $PORT
```

### Paso 4: Plan
- **Free**: $0/mes (duerme después de 15min)
- **Starter**: $7/mes (siempre activo)

### Paso 5: Variables de Entorno
En **Environment**, agregar:

```bash
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PYTHON_VERSION=3.11.0
```

### Paso 6: Deploy
Click **"Create Web Service"** y espera ~5 minutos.

**URL final**: `https://colombian-legal-api.onrender.com`

---

## 📊 Comparación de Servicios

| Característica | Railway | Render | Vercel |
|----------------|---------|--------|--------|
| **Timeout** | ∞ Ilimitado | ∞ Ilimitado | ⚠️ 10s (Free) |
| **Precio Free** | $5 crédito | ✅ Gratis | ✅ Gratis |
| **Cold Start** | ⚡ Rápido | 🐌 Lento | ⚡ Rápido |
| **Python** | ✅ Excelente | ✅ Excelente | ⚠️ Limitado |
| **Scraping** | ✅ Perfecto | ✅ Perfecto | ❌ Malo |
| **Setup** | ⚡ Fácil | ⚡ Fácil | ⚡ Fácil |
| **Recomendado** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 Recomendación Final

### Para tu proyecto (scraping intensivo):

**🥇 Railway**: Mejor opción
- Sin timeout
- Rápido
- Fácil
- $5 gratis

**🥈 Render**: Buena alternativa
- Sin timeout
- Gratis (con limitación de sleep)
- Más lento

**🥉 Vercel**: Solo para consultas
- Solo si no vas a usar `/scrape`
- Perfecto para API de solo lectura

---

## 🧪 Probar el Deploy

Una vez deployado, prueba:

```bash
# Reemplaza con tu URL de Railway/Render
API_URL="https://tu-app.up.railway.app"

# Health check
curl $API_URL/health

# Ver docs
open $API_URL/docs

# Scrape leyes (SIN LÍMITE DE TIMEOUT ✅)
curl -X POST $API_URL/scrape \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "max_laws": 5}' \
  --max-time 300  # 5 minutos OK!

# Buscar
curl -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query": "impuestos", "limit": 10}'
```

---

## 🔧 Troubleshooting

### Railway

```bash
# Ver logs en tiempo real
railway logs --follow

# SSH al contenedor
railway shell

# Ver variables
railway variables

# Restart
railway up --detach
```

### Render

- Logs: Dashboard → Logs tab
- Restart: Dashboard → Manual Deploy → "Clear build cache & deploy"
- Shell: No disponible en plan free

---

## 💰 Costos Estimados

### Railway
- **Free**: $5 de crédito (suficiente para testing)
- **Uso real**: ~$5-10/mes dependiendo del tráfico
- Cobra por uso: $0.000231/GB-hour

### Render
- **Free**: Gratis (sleep después de 15min)
- **Starter**: $7/mes (siempre activo)
- **Pro**: $25/mes (más recursos)

---

## 🎉 ¡Listo para Deploy!

**Archivos creados**:
- ✅ `Procfile` - Comando de inicio
- ✅ `railway.json` - Config de Railway
- ✅ `runtime.txt` - Versión de Python
- ✅ `requirements-deploy.txt` - Dependencias

**Siguiente paso**:
1. Commitear estos archivos
2. Ir a https://railway.app/
3. Deploy en 2 clicks

**¿Necesitas ayuda?** Avísame en qué paso estás.
