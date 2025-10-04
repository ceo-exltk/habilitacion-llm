#!/bin/bash

# Script para verificar que los límites de tokens están correctamente configurados
# Sistema de Agentes LLM Personalizables

echo "🔍 Verificando configuración de límites de tokens..."

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: No se encontró el archivo main.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

echo ""
echo "📊 Verificación de configuración:"
echo "================================="

# 1. Verificar UserAgentConfig
echo "1. UserAgentConfig (user_agent.py):"
echo "   - Valor por defecto:"
grep -n "max_tokens.*Field.*default=" backend/api/models/user_agent.py
echo "   - Límite máximo:"
grep -n "le=" backend/api/models/user_agent.py | grep max_tokens

# 2. Verificar UserAgentUpdate
echo ""
echo "2. UserAgentUpdate (user_agent.py):"
echo "   - Límite máximo:"
grep -n "le=" backend/api/models/user_agent.py | grep max_tokens

# 3. Verificar configuración por defecto en servicio
echo ""
echo "3. Configuración por defecto (user_agent_service.py):"
echo "   - Valor por defecto en get_default_config:"
grep -n "max_tokens=" backend/api/services/user_agent_service.py | head -1
echo "   - Valor por defecto en from_dict:"
grep -n "max_tokens=config_data.get" backend/api/services/user_agent_service.py

# 4. Verificar endpoint de modelos
echo ""
echo "4. Endpoint /models (agent_endpoints.py):"
echo "   - Capacidad máxima mostrada:"
grep -n "max_tokens.*:" backend/api/endpoints/agent_endpoints.py | head -1

# 5. Verificar timeout
echo ""
echo "5. Timeout de conexión (gradient_service.py):"
echo "   - Timeout principal:"
grep -n "timeout=" backend/api/services/gradient_service.py | head -1
echo "   - Timeout de test:"
grep -n "timeout=" backend/api/services/gradient_service.py | tail -1

# 6. Verificar presets
echo ""
echo "6. Presets de configuración:"
echo "   - Preset sentencias-judiciales:"
grep -A 5 "sentencias-judiciales" backend/api/endpoints/agent_endpoints.py | grep max_tokens

echo ""
echo "✅ Verificación completada."
echo ""
echo "📋 Resumen esperado:"
echo "   - Valor por defecto: 32000 tokens"
echo "   - Límite máximo: 128000 tokens"
echo "   - Timeout: 120.0 segundos"
echo "   - Capacidad: Hasta 10-12 sentencias de 2-3 páginas"
