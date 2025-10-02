# 🚀 Instrucciones de Configuración - Habilitación LLM

## 📋 Pasos para Completar la Configuración

### 1. Crear Repositorio en GitHub

**Opción A: Via Web (Recomendado)**
1. Ve a [GitHub.com](https://github.com)
2. Haz clic en "New repository"
3. Nombre: `habilitacion-llm`
4. Descripción: `Sistema de agentes legales personalizables con LLM`
5. Visibilidad: **Público**
6. **NO** inicializar con README, .gitignore o licencia
7. Haz clic en "Create repository"

**Opción B: Via CLI (si tienes GitHub CLI instalado)**
```bash
gh repo create ceo-exltk/habilitacion-llm --public --description "Sistema de agentes legales personalizables con LLM" --source=. --remote=origin --push
```

### 2. Configurar Repositorio Remoto

Después de crear el repositorio en GitHub:

```bash
# Configurar el repositorio remoto
git remote add origin https://github.com/ceo-exltk/habilitacion-llm.git

# Hacer push del código
git push -u origin main
```

### 3. Configurar Secretos en GitHub

Ve a la configuración del repositorio en GitHub:
1. Settings → Secrets and variables → Actions
2. Agregar los siguientes secretos:

#### Secretos Requeridos:
- `DIGITALOCEAN_ACCESS_TOKEN`: Tu token de acceso de DigitalOcean
- `DO_GRADIENT_INFERENCE_KEY`: `sk-do-tMbhJd4J9lY7wtTTVgpwL4uyQNIPcf34v5w5vqLrM2woXbH5Z1Z_SOQDld`
- `SUPABASE_URL`: `https://arixuftpeoplurjavqnb.supabase.co`
- `SUPABASE_ANON_KEY`: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyaXh1ZnRwZW9wbHVyamF2cW5iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNzE4MjMsImV4cCI6MjA3MjY0NzgyM30.jrFg5VxrHdyYablCWuC0YbbQSa7sqMhm5biFdrN1Kmw`
- `SUPABASE_SERVICE_KEY`: `EV[1:tKFaiXTcwxser9LqgxFu8crSBQjYmSKW:JQsld9UjkE35n+OomYUXdO/zgU+TPUs7EcL7jO8fkyJ3SUzX7SHG4z8LjEFd3DWRaVujdX+zcQXQC2+PX3j9Etnl1zn5+UKIAdQxf3sgcWsqXwBEkToB4LNVUc/aL3kM7XPeqyjMt1STiIiTRWlW1dkVtXwJilLYpO4BKiMXrtRz4FLQ17jKnGKO7lkOUCW1oXqi9R3x7EEknZS6oH+XeMoNGCkoMJM3qLmkiC/Dj/qDEXm5giJskCNqqhjoJFtArAkB26N3azsRNsSG3fiKjpKfybCSxtRYB9f/Vi9SJvx9lSSZvGjQI1Qk5w==]`
- `SECRET_KEY`: `habilitacion-llm-super-secret-key-2024`

### 4. Desplegar en DigitalOcean

**Opción A: Automático (Recomendado)**
- El GitHub Actions se ejecutará automáticamente después del push
- Ve a la pestaña "Actions" en GitHub para monitorear el despliegue

**Opción B: Manual**
```bash
# Instalar doctl si no lo tienes
# brew install doctl (macOS)
# o descargar desde: https://github.com/digitalocean/doctl/releases

# Autenticar con DigitalOcean
doctl auth init

# Crear la aplicación
doctl apps create --spec .do/app.yaml
```

### 5. Verificar Despliegue

Una vez desplegado, podrás acceder a:
- **API**: `https://habilitacion-llm-agents-xxxxx.ondigitalocean.app`
- **Documentación**: `https://habilitacion-llm-agents-xxxxx.ondigitalocean.app/docs`
- **Health Check**: `https://habilitacion-llm-agents-xxxxx.ondigitalocean.app/health`

### 6. Probar Endpoints

```bash
# Health check
curl https://habilitacion-llm-agents-xxxxx.ondigitalocean.app/health

# Crear configuración de usuario
curl -X POST https://habilitacion-llm-agents-xxxxx.ondigitalocean.app/api/v1/agent/config/test_user \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "specialization": "penal",
    "tone": "formal",
    "temperature": 0.8
  }'

# Chat con agente
curl -X POST https://habilitacion-llm-agents-xxxxx.ondigitalocean.app/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Cuáles son los elementos del delito de robo?",
    "user_id": "test_user"
  }'
```

## 📊 Estado Actual

- ✅ **Código completo** y funcional
- ✅ **GitHub Actions** configurado
- ✅ **Configuración de App Platform** lista
- ✅ **Testing local** exitoso
- 🔄 **Pendiente**: Crear repositorio en GitHub
- 🔄 **Pendiente**: Configurar secretos
- 🔄 **Pendiente**: Desplegar y probar

## 🎯 Próximos Pasos

1. Crear repositorio en GitHub
2. Configurar secretos
3. Hacer push del código
4. Monitorear despliegue
5. Probar endpoints remotos
6. Comenzar FASE 1 (Arquitectura avanzada)
