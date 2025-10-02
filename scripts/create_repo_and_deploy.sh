#!/bin/bash

# Script para crear repositorio y desplegar
# Sistema de Agentes LLM Personalizables

set -e

echo "🚀 Creando repositorio y desplegando..."

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: No se encontró el archivo main.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

echo "📊 Estado actual del repositorio:"
git status

echo ""
echo "🔧 Configuración actual:"
echo "   - Commits: $(git rev-list --count HEAD)"
echo "   - Archivos: $(git ls-files | wc -l)"
echo "   - Rama actual: $(git branch --show-current)"

echo ""
echo "🌐 CREAR REPOSITORIO EN GITHUB:"
echo ""
echo "1. Ve a https://github.com/new"
echo "2. Nombre: habilitacion-llm"
echo "3. Descripción: Sistema de agentes legales personalizables con LLM"
echo "4. Visibilidad: Público"
echo "5. NO inicializar con README, .gitignore o licencia"
echo "6. Haz clic en 'Create repository'"
echo ""

# Esperar confirmación del usuario
read -p "¿Has creado el repositorio en GitHub? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Por favor crea el repositorio en GitHub primero"
    exit 1
fi

echo "✅ Repositorio creado en GitHub"

# Configurar repositorio remoto
echo ""
echo "🔗 Configurando repositorio remoto..."

# Verificar si ya existe el remoto
if git remote get-url origin > /dev/null 2>&1; then
    echo "   - Remoto 'origin' ya configurado"
else
    git remote add origin https://github.com/ceo-exltk/habilitacion-llm.git
    echo "   - Remoto 'origin' configurado"
fi

# Hacer push del código
echo ""
echo "📤 Haciendo push del código..."
git push -u origin main

echo "✅ Código subido a GitHub"

# Verificar si doctl está instalado
if command -v doctl &> /dev/null; then
    echo ""
    echo "🔧 doctl encontrado, verificando autenticación..."
    
    if doctl account get > /dev/null 2>&1; then
        echo "✅ Autenticado con DigitalOcean"
        
        # Crear aplicación en DigitalOcean
        echo ""
        echo "🚀 Creando aplicación en DigitalOcean App Platform..."
        
        # Verificar si la aplicación ya existe
        if doctl apps list --format "Name" --no-header | grep -q "habilitacion-llm-agents"; then
            echo "⚠️  La aplicación 'habilitacion-llm-agents' ya existe"
            echo "   Actualizando configuración..."
            doctl apps update $(doctl apps list --format "ID,Name" --no-header | grep "habilitacion-llm-agents" | awk '{print $1}') --spec .do/app.yaml
        else
            echo "   Creando nueva aplicación..."
            doctl apps create --spec .do/app.yaml
        fi
        
        echo "✅ Aplicación creada/actualizada en DigitalOcean"
        
        # Esperar un momento para que se despliegue
        echo ""
        echo "⏳ Esperando que se complete el despliegue..."
        sleep 30
        
        # Obtener información de la aplicación
        echo ""
        echo "📊 Información de la aplicación:"
        APP_ID=$(doctl apps list --format "ID,Name" --no-header | grep "habilitacion-llm-agents" | awk '{print $1}' | head -1)
        
        if [ -n "$APP_ID" ]; then
            doctl apps get $APP_ID --format "ID,Name,DefaultIngress,ActiveDeployment.Status"
            
            # Obtener la URL
            APP_URL=$(doctl apps get $APP_ID --format "DefaultIngress" --no-header)
            
            if [ -n "$APP_URL" ] && [ "$APP_URL" != "<nil>" ]; then
                echo ""
                echo "🎉 ¡Despliegue completado!"
                echo "   URL: $APP_URL"
                echo "   Docs: $APP_URL/docs"
                echo "   Health: $APP_URL/health"
                
                # Probar endpoints
                echo ""
                echo "🧪 Probando endpoints..."
                
                # Health check
                if curl -s -f "$APP_URL/health" > /dev/null; then
                    echo "   ✅ Health check exitoso"
                else
                    echo "   ❌ Health check falló"
                fi
                
                # Agent health
                if curl -s -f "$APP_URL/api/v1/agent/health" > /dev/null; then
                    echo "   ✅ Agent health exitoso"
                else
                    echo "   ❌ Agent health falló"
                fi
                
            else
                echo "⚠️  La aplicación aún no tiene URL asignada"
                echo "   Verifica el estado en: https://cloud.digitalocean.com/apps"
            fi
        else
            echo "❌ No se pudo encontrar la aplicación"
        fi
        
    else
        echo "❌ No autenticado con DigitalOcean"
        echo "   Ejecuta: doctl auth init"
        echo "   Luego ejecuta este script nuevamente"
    fi
else
    echo "⚠️  doctl no está instalado"
    echo "   Instala con: brew install doctl (macOS)"
    echo "   O descarga desde: https://github.com/digitalocean/doctl/releases"
    echo ""
    echo "📋 Pasos manuales para desplegar:"
    echo "1. Instala doctl"
    echo "2. Autentica: doctl auth init"
    echo "3. Crea app: doctl apps create --spec .do/app.yaml"
    echo "4. Prueba: ./scripts/test_deployment.sh"
fi

echo ""
echo "🎯 Próximos pasos:"
echo "1. Configurar secretos en GitHub (Settings → Secrets and variables → Actions)"
echo "2. Verificar que el GitHub Actions se ejecute correctamente"
echo "3. Probar todos los endpoints"
echo "4. Comenzar FASE 1 (Arquitectura avanzada)"
echo ""
echo "📚 Para más detalles, consulta: SETUP_INSTRUCTIONS.md"
