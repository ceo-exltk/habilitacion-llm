#!/bin/bash

# Script de inicio para desarrollo local
# Sistema de Agentes LLM Personalizables

set -e

echo "🚀 Iniciando servidor de desarrollo..."

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: No se encontró el archivo main.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

# Cambiar al directorio backend
cd backend

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar que pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Cargar variables de entorno
if [ -f "config.env" ]; then
    echo "🔑 Cargando variables de entorno..."
    export $(cat config.env | grep -v '^#' | xargs)
fi

# Verificar que las variables de entorno están configuradas
if [ -z "$DO_GRADIENT_INFERENCE_KEY" ]; then
    echo "⚠️  Advertencia: DO_GRADIENT_INFERENCE_KEY no está configurada"
fi

if [ -z "$SUPABASE_URL" ]; then
    echo "⚠️  Advertencia: SUPABASE_URL no está configurada"
fi

# Iniciar servidor
echo "🌐 Iniciando servidor FastAPI..."
echo "   URL: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo "   Health: http://localhost:8000/health"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
