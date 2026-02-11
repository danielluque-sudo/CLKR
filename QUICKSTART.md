# ⚡ QUICKSTART - Deploy en 5 Minutos

---

## 🎯 Opción más rápida: Railway

### 1️⃣ Ve a Railway
👉 **https://railway.app/new**

### 2️⃣ Deploy from GitHub
```
1. Click "Deploy from GitHub repo"
2. Conecta tu cuenta de GitHub
3. Selecciona: danielluque-sudo/CLKR
4. Railway hace el resto automáticamente ✨
```

### 3️⃣ Agrega Variables de Entorno
En el dashboard → **Variables** → **RAW Editor**:

```env
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

💡 **Tip**: Copia los valores desde tu archivo `.env` local

### 4️⃣ ¡Listo! 🎉

Tu API estará en: `https://[tu-proyecto].up.railway.app`

**Pruébala:**
```bash
curl https://[tu-proyecto].up.railway.app/health
```

**Ver documentación interactiva:**
```
https://[tu-proyecto].up.railway.app/docs
```

---

## 🧪 Prueba tu API

```bash
# Salud
curl https://tu-url/health

# Scrape 3 leyes de 2023 (SIN LÍMITE DE TIMEOUT!)
curl -X POST https://tu-url/scrape \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "max_laws": 3}'

# Buscar leyes
curl -X POST https://tu-url/search \
  -H "Content-Type: application/json" \
  -d '{"query": "sistema nacional", "limit": 5}'

# Ver leyes en la base de datos
curl https://tu-url/laws?year=2023&limit=10
```

---

## 📱 Usando desde JavaScript/Frontend

```javascript
// Scrape leyes
const response = await fetch('https://tu-url/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ year: 2023, max_laws: 5 })
});
const laws = await response.json();
console.log(laws);
```

---

## 🐍 Usando desde Python

```python
import requests

# Scrape
response = requests.post('https://tu-url/scrape', json={
    'year': 2023,
    'max_laws': 5
})
laws = response.json()
print(laws)
```

---

## 📚 Más Información

- **Railway completo**: `RAILWAY_RENDER_DEPLOYMENT.md`
- **Render alternativo**: `RAILWAY_RENDER_DEPLOYMENT.md`
- **Vercel (no recomendado para scraping)**: `VERCEL_DEPLOYMENT.md`

---

## 💰 Costos

**Railway**: $5 gratis → suficiente para testing completo
**Render**: Gratis (sleep 15min) o $7/mes siempre activo
**Vercel**: Gratis pero limitado (10s timeout)

---

## ❓ Ayuda

**Problema con Railway?**
```bash
# Ver logs
railway logs --follow

# Reiniciar
railway up --detach
```

**Problema con Render?**
- Dashboard → Logs tab
- Manual Deploy → "Clear build cache & deploy"

---

## ✅ Checklist

- [ ] Cuenta en Railway creada
- [ ] Repo conectado
- [ ] Variables de entorno configuradas
- [ ] Deploy exitoso
- [ ] Probado `/health`
- [ ] Probado `/docs`
- [ ] Probado `/scrape`

---

## 🎉 ¡Listo!

Tu API de leyes colombianas está en producción y lista para usar.

**Sin límite de timeout** → Scraping perfecto ✅
**Deploy automático** → Cada push actualiza ✅
**SSL gratis** → HTTPS incluido ✅
**Logs en tiempo real** → Debug fácil ✅
