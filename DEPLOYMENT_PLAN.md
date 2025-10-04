# 🚀 Plan de Despliegue - Límites de Tokens para Múltiples Sentencias

## 📋 Resumen
Actualización de la aplicación para procesar múltiples sentencias judiciales simultáneamente, ampliando los límites de tokens de 4,000 a 32,000 (por defecto) y hasta 128,000 (máximo).

## 🎯 Objetivo
Permitir el procesamiento de hasta **10-12 sentencias judiciales** de 2-3 páginas cada una en una sola consulta.

## ✅ Cambios Aplicados

### 1. **Modelos de Datos** (`user_agent.py`)
- ✅ **Valor por defecto**: `32,000 tokens` (antes 1,000)
- ✅ **Límite máximo**: `128,000 tokens` (antes 4,000)
- ✅ **Validación**: `ge=1, le=128000`

### 2. **Servicios** (`user_agent_service.py`)
- ✅ **Configuración por defecto**: `32,000 tokens`
- ✅ **Valor de fallback**: `32,000 tokens` (antes 1,000)

### 3. **Servicio Gradient AI** (`gradient_service.py`)
- ✅ **Timeout principal**: `120 segundos` (antes 30)
- ✅ **Test de conexión**: `50 tokens` (antes 10)

### 4. **Endpoints** (`agent_endpoints.py`)
- ✅ **Endpoint /models**: Muestra `128,000` como capacidad máxima
- ✅ **Preset sentencias**: `32,000 tokens` por defecto
- ✅ **Presets adicionales**: Configuraciones escaladas

## 📊 Capacidades por Escenario

| Escenario | Sentencias | Páginas | Tokens | Configuración |
|-----------|------------|---------|--------|---------------|
| **Básico** | 1-3 | 2-9 | 5,000-15,000 | Por defecto (32K) |
| **Estándar** | 5-8 | 10-24 | 20,000-32,000 | Por defecto (32K) |
| **Avanzado** | 10-12 | 20-36 | 40,000-48,000 | Por defecto (32K) |
| **Extremo** | 15+ | 30+ | 60,000+ | Manual (64K-128K) |

## 🔧 Scripts de Despliegue

### 1. **Verificación** (Ya ejecutado)
```bash
./scripts/verify_token_limits.sh
```
**Estado**: ✅ Completado - Todos los cambios verificados

### 2. **Despliegue Local** (Opcional)
```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### 3. **Despliegue a Producción**
```bash
./scripts/deploy.sh
```

## 🧪 Pruebas Recomendadas

### 1. **Prueba Básica** (1-3 sentencias)
```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analiza estas 3 sentencias: [contenido de 3 sentencias]",
    "user_id": "test_user"
  }'
```

### 2. **Prueba Estándar** (5-8 sentencias)
```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compara estas 8 sentencias: [contenido de 8 sentencias]",
    "user_id": "test_user"
  }'
```

### 3. **Prueba de Límite** (10+ sentencias)
```bash
curl -X PUT "http://localhost:8000/api/v1/agent/config/test_user" \
  -H "Content-Type: application/json" \
  -d '{"max_tokens": 64000}'
```

## 📈 Monitoreo Post-Despliegue

### 1. **Métricas a Observar**
- Tiempo de respuesta promedio
- Uso de tokens por consulta
- Tasa de errores de timeout
- Costos de API

### 2. **Alertas Recomendadas**
- Timeout > 100 segundos
- Uso de tokens > 100,000 por consulta
- Tasa de error > 5%

## ⚠️ Consideraciones Importantes

### 1. **Costos**
- **32K tokens** ≈ 2-3x más caro que 4K tokens
- **128K tokens** ≈ 8-10x más caro que 4K tokens
- Monitorear uso y ajustar según presupuesto

### 2. **Rendimiento**
- Respuestas más largas = mayor tiempo de procesamiento
- Timeout de 120s debería ser suficiente
- Considerar procesamiento asíncrono para casos extremos

### 3. **Límites del Modelo**
- `openai-gpt-oss-120b` soporta hasta 128,000 tokens
- Configuración actual está dentro de los límites
- No requiere cambio de modelo

## 🎯 Próximos Pasos

1. **Desplegar a producción** usando `./scripts/deploy.sh`
2. **Ejecutar pruebas** con diferentes volúmenes de sentencias
3. **Monitorear métricas** durante las primeras 24-48 horas
4. **Ajustar configuración** según el uso real observado

## 📞 Soporte

Si encuentras problemas:
1. Verificar logs de la aplicación
2. Revisar métricas de uso de tokens
3. Ajustar timeout si es necesario
4. Considerar procesamiento por lotes para casos extremos

---
**Estado**: ✅ Listo para despliegue
**Fecha**: $(date)
**Versión**: 1.0.0
