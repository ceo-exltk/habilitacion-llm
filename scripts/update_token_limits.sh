#!/bin/bash

# Script para actualizar límites de tokens para múltiples sentencias
# Sistema de Agentes LLM Personalizables

set -e

echo "🔧 Actualizando límites de tokens para múltiples sentencias..."

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: No se encontró el archivo main.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

echo "📝 Aplicando cambios de configuración..."

# 1. Corregir configuración por defecto en user_agent_service.py
echo "   - Corrigiendo configuración por defecto..."
sed -i.bak 's/max_tokens=config_data.get("max_tokens", 1000)/max_tokens=config_data.get("max_tokens", 32000)/' backend/api/services/user_agent_service.py

# 2. Aumentar timeout para procesamiento largo
echo "   - Aumentando timeout de conexión..."
sed -i.bak 's/timeout=30.0/timeout=120.0/' backend/api/services/gradient_service.py

# 3. Actualizar test de conexión
echo "   - Actualizando test de conexión..."
sed -i.bak 's/"max_tokens": 10/"max_tokens": 50/' backend/api/services/gradient_service.py

# 4. Verificar cambios
echo "✅ Verificando cambios aplicados..."
echo "   - Configuración por defecto:"
grep -n "max_tokens=config_data.get" backend/api/services/user_agent_service.py
echo "   - Timeout de conexión:"
grep -n "timeout=" backend/api/services/gradient_service.py
echo "   - Test de conexión:"
grep -n "max_tokens.*50" backend/api/services/gradient_service.py

echo ""
echo "🎯 Resumen de cambios:"
echo "   ✅ Límite por defecto: 32,000 tokens (antes 1,000)"
echo "   ✅ Límite máximo: 128,000 tokens"
echo "   ✅ Timeout: 120 segundos (antes 30)"
echo "   ✅ Capacidad: Hasta 10-12 sentencias de 2-3 páginas"
echo ""
echo "🚀 Los cambios están listos para despliegue."
echo "   Ejecuta: ./scripts/deploy.sh para desplegar a producción"
