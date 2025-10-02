#!/bin/bash

# Script para configurar el repositorio y desplegar
# Sistema de Agentes LLM Personalizables

set -e

echo "🚀 Configurando repositorio y despliegue..."

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: No se encontró el archivo main.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

# Verificar que git está configurado
if ! git config user.name > /dev/null 2>&1; then
    echo "⚠️  Configurando Git..."
    git config user.name "Alexis Peña"
    git config user.email "alepenavargas@gmail.com"
fi

# Verificar estado del repositorio
echo "📊 Estado del repositorio:"
git status

echo ""
echo "🔧 Configuración actual:"
echo "   - Repositorio local: ✅"
echo "   - Commits: $(git rev-list --count HEAD)"
echo "   - Archivos: $(git ls-files | wc -l)"

echo ""
echo "📋 Próximos pasos manuales:"
echo ""
echo "1. 🌐 Crear repositorio en GitHub:"
echo "   - Ve a https://github.com/new"
echo "   - Nombre: habilitacion-llm"
echo "   - Descripción: Sistema de agentes legales personalizables con LLM"
echo "   - Visibilidad: Público"
echo "   - NO inicializar con README"
echo ""
echo "2. 🔗 Configurar repositorio remoto:"
echo "   git remote add origin https://github.com/ceo-exltk/habilitacion-llm.git"
echo "   git push -u origin main"
echo ""
echo "3. 🔐 Configurar secretos en GitHub:"
echo "   - Ve a Settings → Secrets and variables → Actions"
echo "   - Agrega los secretos listados en SETUP_INSTRUCTIONS.md"
echo ""
echo "4. 🚀 Desplegar:"
echo "   - El GitHub Actions se ejecutará automáticamente"
echo "   - O manualmente: doctl apps create --spec .do/app.yaml"
echo ""

# Verificar si doctl está instalado
if command -v doctl &> /dev/null; then
    echo "✅ doctl está instalado"
    
    # Verificar autenticación
    if doctl account get > /dev/null 2>&1; then
        echo "✅ Autenticado con DigitalOcean"
        
        # Mostrar aplicaciones existentes
        echo ""
        echo "📱 Aplicaciones existentes en DigitalOcean:"
        doctl apps list --format "ID,Name,DefaultIngress,ActiveDeployment.Status" 2>/dev/null || echo "   No se pudieron obtener las aplicaciones"
    else
        echo "⚠️  No autenticado con DigitalOcean"
        echo "   Ejecuta: doctl auth init"
    fi
else
    echo "⚠️  doctl no está instalado"
    echo "   Instala con: brew install doctl (macOS)"
    echo "   O descarga desde: https://github.com/digitalocean/doctl/releases"
fi

echo ""
echo "🎯 Una vez completados los pasos manuales, ejecuta:"
echo "   ./scripts/test_deployment.sh"
echo ""
echo "📚 Para más detalles, consulta: SETUP_INSTRUCTIONS.md"
