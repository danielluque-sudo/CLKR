# 🚀 Despliegue en Vercel

## Guía paso a paso para deployar tu API de leyes colombianas

---

## 📋 Pre-requisitos

1. **Cuenta en Vercel**: https://vercel.com/signup
2. **Credenciales configuradas**:
   - Supabase URL y Key
   - Anthropic API Key (opcional pero recomendado)

---

## 🔧 Método 1: Deploy con CLI de Vercel (Recomendado)

### Paso 1: Instalar Vercel CLI

```bash
npm install -g vercel
# o
pnpm install -g vercel
```

### Paso 2: Login en Vercel

```bash
vercel login
```

### Paso 3: Deploy desde el directorio del proyecto

```bash
cd /home/user/CLKR
vercel
```

Sigue las instrucciones:
- **Set up and deploy?** → Yes
- **Which scope?** → Tu cuenta personal
- **Link to existing project?** → No (primera vez)
- **Project name?** → colombian-legal-api
- **Directory?** → ./ (presiona Enter)
- **Override settings?** → No

### Paso 4: Configurar variables de entorno

```bash
# En la terminal o en el dashboard de Vercel
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add ANTHROPIC_API_KEY
```

O configúralas en el dashboard: https://vercel.com/tu-usuario/colombian-legal-api/settings/environment-variables

### Paso 5: Re-deploy con las variables

```bash
vercel --prod
```

---

## 🌐 Método 2: Deploy desde GitHub (Más fácil)

### Paso 1: Ve a Vercel Dashboard

https://vercel.com/new

### Paso 2: Importa tu repositorio

1. Click en **"Import Project"**
2. Selecciona **GitHub**
3. Busca: `danielluque-sudo/CLKR`
4. Click **"Import"**

### Paso 3: Configuración del proyecto

```
Framework Preset: Other
Root Directory: ./
Build Command: (dejar vacío)
Output Directory: (dejar vacío)
Install Command: pip install -r requirements-vercel.txt
```

### Paso 4: Variables de entorno

En **"Environment Variables"**, agrega:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://qkyojpaawsdckzixzqnd.supabase.co` |
| `SUPABASE_KEY` | `sb_publishable_38nUetGLXCCPO-bYAmdSBg_zwI1EyQD` |
| `ANTHROPIC_API_KEY` | `sk-ant-api03-xIj...` (tu key completa) |

### Paso 5: Deploy

Click **"Deploy"** y espera ~2 minutos.

---

## ✅ Verificar el deployment

Una vez deployado, tu API estará en:

```
https://colombian-legal-api.vercel.app
```

### Probar endpoints:

```bash
# Health check
curl https://tu-app.vercel.app/health

# Ver documentación interactiva
open https://tu-app.vercel.app/docs

# Probar scraping (puede tardar)
curl -X POST https://tu-app.vercel.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "max_laws": 2}'

# Buscar leyes en la base de datos
curl https://tu-app.vercel.app/laws?year=2023&limit=5
```

---

## 📊 Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Home page con info de la API |
| `/health` | GET | Health check |
| `/docs` | GET | Documentación interactiva (Swagger) |
| `/scrape` | POST | Scrapea leyes de un año específico |
| `/laws` | GET | Lista leyes de la base de datos |
| `/laws/{law_number}` | GET | Obtiene una ley específica |
| `/search` | POST | Busca leyes por keyword |
| `/stats` | GET | Estadísticas de la base de datos |

---

## 🧪 Ejemplo de uso con JavaScript

```javascript
// Scrape laws
const response = await fetch('https://tu-app.vercel.app/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    year: 2023,
    max_laws: 5
  })
});

const laws = await response.json();
console.log(laws);

// Search laws
const searchResponse = await fetch('https://tu-app.vercel.app/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'impuestos',
    limit: 10
  })
});

const results = await searchResponse.json();
console.log(results);
```

---

## 🧪 Ejemplo de uso con Python

```python
import requests

# Scrape laws
response = requests.post('https://tu-app.vercel.app/scrape', json={
    'year': 2023,
    'max_laws': 5
})

laws = response.json()
print(laws)

# Search laws
response = requests.post('https://tu-app.vercel.app/search', json={
    'query': 'impuestos',
    'limit': 10
})

results = response.json()
print(results)
```

---

## ⚠️ Limitaciones de Vercel

| Limitación | Free Tier | Pro Tier |
|------------|-----------|----------|
| **Timeout** | 10 segundos | 60 segundos |
| **Memoria** | 1024 MB | 3008 MB |
| **Requests/día** | ~100K | Ilimitado |

**⚠️ IMPORTANTE**: El scraping puede tardar más de 10 segundos, así que en el plan gratuito puede fallar. Considera:

1. **Usar el plan Pro** ($20/mes) para timeouts de 60s
2. **Scraping asíncrono**: El scraping se ejecuta en background, la API retorna de inmediato
3. **Scraping local**: Ejecuta el scraper localmente y usa Vercel solo para consultas

---

## 🎯 Configuración recomendada

### Para consultas rápidas (< 10s):
✅ Vercel Free Tier funciona perfecto
- `/health`
- `/laws`
- `/search`
- `/stats`

### Para scraping (> 10s):
❌ Vercel Free Tier puede fallar
✅ Opciones:
1. Actualizar a Vercel Pro
2. Usar Vercel + Background Jobs
3. Deployar en Railway/Render (sin límite de tiempo)
4. Scraping local + API en Vercel solo para consultas

---

## 🔄 Alternativa: Railway (Sin timeout)

Si el scraping es demasiado lento para Vercel:

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

Railway no tiene límite de timeout y es mejor para scraping intensivo.

---

## 🎉 ¡Listo!

Ahora tienes una API REST desplegada que puede:
- ✅ Scrapear leyes colombianas
- ✅ Procesar con IA
- ✅ Almacenar en Supabase
- ✅ Buscar y consultar leyes
- ✅ Acceso público via HTTPS

**URL de tu API**: https://colombian-legal-api-[tu-usuario].vercel.app

**Documentación**: https://colombian-legal-api-[tu-usuario].vercel.app/docs
