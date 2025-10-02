#!/bin/bash

# Script para probar el despliegue en DigitalOcean
# Sistema de Agentes LLM Personalizables

set -e

echo "🧪 Probando despliegue en DigitalOcean..."

# Verificar que doctl está instalado
if ! command -v doctl &> /dev/null; then
    echo "❌ Error: doctl no está instalado"
    echo "   Instala con: brew install doctl (macOS)"
    exit 1
fi

# Verificar autenticación
if ! doctl account get > /dev/null 2>&1; then
    echo "❌ Error: No autenticado con DigitalOcean"
    echo "   Ejecuta: doctl auth init"
    exit 1
fi

echo "✅ Autenticado con DigitalOcean"

# Buscar la aplicación
echo "🔍 Buscando aplicación habilitacion-llm-agents..."

APP_ID=$(doctl apps list --format "ID,Name" --no-header | grep "habilitacion-llm-agents" | awk '{print $1}' | head -1)

if [ -z "$APP_ID" ]; then
    echo "❌ No se encontró la aplicación habilitacion-llm-agents"
    echo "   Creando aplicación..."
    
    # Crear la aplicación
    doctl apps create --spec .do/app.yaml
    
    # Esperar un momento
    echo "⏳ Esperando que se cree la aplicación..."
    sleep 10
    
    # Buscar nuevamente
    APP_ID=$(doctl apps list --format "ID,Name" --no-header | grep "habilitacion-llm-agents" | awk '{print $1}' | head -1)
    
    if [ -z "$APP_ID" ]; then
        echo "❌ Error: No se pudo crear la aplicación"
        exit 1
    fi
fi

echo "✅ Aplicación encontrada: $APP_ID"

# Obtener información de la aplicación
echo "📊 Información de la aplicación:"
doctl apps get $APP_ID --format "ID,Name,DefaultIngress,ActiveDeployment.Status"

# Obtener la URL de la aplicación
APP_URL=$(doctl apps get $APP_ID --format "DefaultIngress" --no-header)

if [ -z "$APP_URL" ] || [ "$APP_URL" = "<nil>" ]; then
    echo "⚠️  La aplicación aún no tiene URL asignada"
    echo "   Esperando que se complete el despliegue..."
    
    # Esperar hasta que tenga URL
    for i in {1..30}; do
        APP_URL=$(doctl apps get $APP_ID --format "DefaultIngress" --no-header 2>/dev/null)
        if [ -n "$APP_URL" ] && [ "$APP_URL" != "<nil>" ]; then
            break
        fi
        echo "   Intento $i/30 - Esperando..."
        sleep 10
    done
fi

if [ -z "$APP_URL" ] || [ "$APP_URL" = "<nil>" ]; then
    echo "❌ Error: No se pudo obtener la URL de la aplicación"
    echo "   Verifica el estado en: https://cloud.digitalocean.com/apps"
    exit 1
fi

echo "✅ URL de la aplicación: $APP_URL"

# Probar endpoints
echo ""
echo "🧪 Probando endpoints..."

# Test 1: Health check
echo "1. Probando health check..."
if curl -s -f "$APP_URL/health" > /dev/null; then
    echo "   ✅ Health check exitoso"
    curl -s "$APP_URL/health" | jq '.' 2>/dev/null || curl -s "$APP_URL/health"
else
    echo "   ❌ Health check falló"
fi

# Test 2: Agent health
echo ""
echo "2. Probando health del agente..."
if curl -s -f "$APP_URL/api/v1/agent/health" > /dev/null; then
    echo "   ✅ Agent health exitoso"
    curl -s "$APP_URL/api/v1/agent/health" | jq '.' 2>/dev/null || curl -s "$APP_URL/api/v1/agent/health"
else
    echo "   ❌ Agent health falló"
fi

# Test 3: Crear configuración de usuario
echo ""
echo "3. Probando creación de configuración de usuario..."
USER_CONFIG_RESPONSE=$(curl -s -X POST "$APP_URL/api/v1/agent/config/test_user_remote" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_remote",
    "specialization": "penal",
    "tone": "formal",
    "temperature": 0.8,
    "max_tokens": 1500,
    "custom_instructions": "Eres un experto en derecho penal con 20 años de experiencia."
  }')

if echo "$USER_CONFIG_RESPONSE" | grep -q "user_id"; then
    echo "   ✅ Configuración de usuario creada exitosamente"
    echo "$USER_CONFIG_RESPONSE" | jq '.' 2>/dev/null || echo "$USER_CONFIG_RESPONSE"
else
    echo "   ❌ Error creando configuración de usuario"
    echo "$USER_CONFIG_RESPONSE"
fi

# Test 4: Chat con agente
echo ""
echo "4. Probando chat con agente..."
CHAT_RESPONSE=$(curl -s -X POST "$APP_URL/api/v1/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Cuáles son los elementos del delito de robo?",
    "user_id": "test_user_remote",
    "context": "Consulta legal sobre derecho penal"
  }')

if echo "$CHAT_RESPONSE" | grep -q "response"; then
    echo "   ✅ Chat con agente exitoso"
    echo "$CHAT_RESPONSE" | jq '.response' 2>/dev/null || echo "Respuesta recibida (formato no JSON)"
else
    echo "   ❌ Error en chat con agente"
    echo "$CHAT_RESPONSE"
fi

# Test 5: Documentación
echo ""
echo "5. Probando documentación..."
if curl -s -f "$APP_URL/docs" > /dev/null; then
    echo "   ✅ Documentación disponible en: $APP_URL/docs"
else
    echo "   ❌ Documentación no disponible"
fi

echo ""
echo "🎉 Pruebas completadas!"
echo ""
echo "📱 Enlaces útiles:"
echo "   - Aplicación: $APP_URL"
echo "   - Documentación: $APP_URL/docs"
echo "   - Health: $APP_URL/health"
echo "   - Agent Health: $APP_URL/api/v1/agent/health"
echo ""
echo "🔧 Para monitorear la aplicación:"
echo "   doctl apps logs $APP_ID"
echo "   doctl apps get $APP_ID"
