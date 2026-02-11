#!/bin/bash
# deploy.sh - Script interactivo para deployar en Railway o Render

echo "🚀 COLOMBIAN LEGAL SCRAPER - DEPLOYMENT HELPER"
echo "=============================================="
echo ""
echo "Este script te ayudará a deployar tu API."
echo ""
echo "Opciones disponibles:"
echo "  1) Railway (Recomendado - Sin límite de timeout)"
echo "  2) Render (Alternativa - Plan gratuito disponible)"
echo "  3) Vercel (Solo consultas - Timeout 10s)"
echo "  4) Salir"
echo ""
read -p "Selecciona una opción (1-4): " choice

case $choice in
  1)
    echo ""
    echo "🚂 DEPLOYANDO EN RAILWAY"
    echo "========================"
    echo ""
    echo "Paso 1: Instalar Railway CLI"
    echo "  npm i -g @railway/cli"
    echo ""
    read -p "¿Ya tienes Railway CLI instalado? (y/n): " has_cli

    if [ "$has_cli" != "y" ]; then
      echo "Instalando Railway CLI..."
      npm i -g @railway/cli
    fi

    echo ""
    echo "Paso 2: Login en Railway"
    railway login

    echo ""
    echo "Paso 3: Inicializar proyecto"
    railway init

    echo ""
    echo "Paso 4: Configurar variables de entorno"
    echo "Leyendo desde .env..."

    if [ -f .env ]; then
      source .env
      railway variables set SUPABASE_URL="$SUPABASE_URL"
      railway variables set SUPABASE_KEY="$SUPABASE_KEY"
      railway variables set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
      echo "✅ Variables configuradas"
    else
      echo "⚠️  Archivo .env no encontrado"
      echo "Configura manualmente:"
      echo "  railway variables set SUPABASE_URL=..."
      echo "  railway variables set SUPABASE_KEY=..."
      echo "  railway variables set ANTHROPIC_API_KEY=..."
    fi

    echo ""
    echo "Paso 5: Deploy"
    railway up

    echo ""
    echo "✅ Deploy completado!"
    echo ""
    echo "Ver logs: railway logs"
    echo "Abrir en navegador: railway open"
    ;;

  2)
    echo ""
    echo "🎨 DEPLOYANDO EN RENDER"
    echo "======================="
    echo ""
    echo "Render requiere deploy manual desde el dashboard."
    echo ""
    echo "Sigue estos pasos:"
    echo ""
    echo "1. Ve a: https://render.com/"
    echo "2. Click en 'New +' → 'Web Service'"
    echo "3. Conecta GitHub y selecciona tu repo: danielluque-sudo/CLKR"
    echo "4. Configura:"
    echo "   - Runtime: Python 3"
    echo "   - Build Command: pip install -r requirements-deploy.txt"
    echo "   - Start Command: uvicorn api.app:app --host 0.0.0.0 --port \$PORT"
    echo ""
    echo "5. Agrega estas variables de entorno:"

    if [ -f .env ]; then
      source .env
      echo ""
      echo "   SUPABASE_URL=$SUPABASE_URL"
      echo "   SUPABASE_KEY=$SUPABASE_KEY"
      echo "   ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY"
      echo "   PYTHON_VERSION=3.11.0"
    else
      echo "   (Revisa tu archivo .env)"
    fi

    echo ""
    echo "6. Click en 'Create Web Service'"
    echo ""
    read -p "Presiona Enter cuando hayas terminado..."
    ;;

  3)
    echo ""
    echo "☁️  DEPLOYANDO EN VERCEL"
    echo "======================="
    echo ""
    echo "⚠️  ADVERTENCIA: Vercel tiene timeout de 10 segundos"
    echo "    El endpoint /scrape probablemente fallará."
    echo "    Solo recomendado para endpoints de consulta."
    echo ""
    read -p "¿Estás seguro? (y/n): " confirm

    if [ "$confirm" = "y" ]; then
      echo ""
      read -p "¿Tienes Vercel CLI instalado? (y/n): " has_vercel

      if [ "$has_vercel" != "y" ]; then
        echo "Instalando Vercel CLI..."
        npm i -g vercel
      fi

      echo ""
      echo "Deploying..."
      vercel

      echo ""
      echo "Configura las variables de entorno:"
      echo "  vercel env add SUPABASE_URL"
      echo "  vercel env add SUPABASE_KEY"
      echo "  vercel env add ANTHROPIC_API_KEY"
      echo ""
      echo "Luego ejecuta: vercel --prod"
    fi
    ;;

  4)
    echo "Saliendo..."
    exit 0
    ;;

  *)
    echo "Opción inválida"
    exit 1
    ;;
esac

echo ""
echo "=============================================="
echo "🎉 ¡DEPLOYMENT COMPLETADO!"
echo "=============================================="
echo ""
echo "Prueba tu API:"
echo "  curl https://tu-url/health"
echo "  curl https://tu-url/docs"
echo ""
echo "Lee la documentación completa:"
echo "  - RAILWAY_RENDER_DEPLOYMENT.md"
echo "  - VERCEL_DEPLOYMENT.md"
echo ""
