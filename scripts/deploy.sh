#!/bin/bash

# Script de despliegue para DigitalOcean App Platform
# Sistema de Agentes LLM Personalizables

set -e

echo "🚀 Iniciando despliegue del sistema de agentes LLM..."

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: No se encontró el archivo main.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

# Crear archivo .do/app.yaml para DigitalOcean App Platform
echo "📝 Creando configuración de App Platform..."

mkdir -p .do

cat > .do/app.yaml << EOF
name: habilitacion-llm-agents
services:
- name: api
  source_dir: backend
  github:
    repo: ceo-exltk/habilitacion-llm
    branch: main
  run_command: uvicorn api.main:app --host 0.0.0.0 --port \$PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  envs:
  - key: DO_GRADIENT_INFERENCE_KEY
    value: sk-do-tMbhJd4J9lY7wtTTVgpwL4uyQNIPcf34v5w5vqLrM2woXbH5Z1Z_SOQDld
    scope: RUN_AND_BUILD_TIME
  - key: GRADIENT_BASE_URL
    value: https://inference.do-ai.run
    scope: RUN_AND_BUILD_TIME
  - key: GRADIENT_MODEL
    value: openai-gpt-oss-120b
    scope: RUN_AND_BUILD_TIME
  - key: SUPABASE_URL
    value: https://arixuftpeoplurjavqnb.supabase.co
    scope: RUN_AND_BUILD_TIME
  - key: SUPABASE_ANON_KEY
    value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyaXh1ZnRwZW9wbHVyamF2cW5iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNzE4MjMsImV4cCI6MjA3MjY0NzgyM30.jrFg5VxrHdyYablCWuC0YbbQSa7sqMhm5biFdrN1Kmw
    scope: RUN_AND_BUILD_TIME
  - key: SUPABASE_SERVICE_KEY
    value: EV[1:tKFaiXTcwxser9LqgxFu8crSBQjYmSKW:JQsld9UjkE35n+OomYUXdO/zgU+TPUs7EcL7jO8fkyJ3SUzX7SHG4z8LjEFd3DWRaVujdX+zcQXQC2+PX3j9Etnl1zn5+UKIAdQxf3sgcWsqXwBEkToB4LNVUc/aL3kM7XPeqyjMt1STiIiTRWlW1dkVtXwJilLYpO4BKiMXrtRz4FLQ17jKnGKO7lkOUCW1oXqi9R3x7EEknZS6oH+XeMoNGCkoMJM3qLmkiC/Dj/qDEXm5giJskCNqqhjoJFtArAkB26N3azsRNsSG3fiKjpKfybCSxtRYB9f/Vi9SJvx9lSSZvGjQI1Qk5w==]
    scope: RUN_AND_BUILD_TIME
    type: SECRET
  - key: SECRET_KEY
    value: habilitacion-llm-super-secret-key-2024
    scope: RUN_AND_BUILD_TIME
  - key: DEBUG
    value: false
    scope: RUN_AND_BUILD_TIME
  - key: LOG_LEVEL
    value: INFO
    scope: RUN_AND_BUILD_TIME
  health_check:
    http_path: /health
    initial_delay_seconds: 10
    period_seconds: 10
    timeout_seconds: 5
    success_threshold: 1
    failure_threshold: 3
  routes:
  - path: /
    component:
      name: api
      preserve_path_prefix: false
  - path: /api
    component:
      name: api
      preserve_path_prefix: true
  - path: /docs
    component:
      name: api
      preserve_path_prefix: true
  - path: /redoc
    component:
      name: api
      preserve_path_prefix: true
  - path: /health
    component:
      name: api
      preserve_path_prefix: true
  - path: /api/v1/agent
    component:
      name: api
      preserve_path_prefix: true
region: atl
features:
- buildpack-stack=ubuntu-22
EOF

echo "✅ Configuración de App Platform creada en .do/app.yaml"

# Crear archivo .doignore
echo "📝 Creando archivo .doignore..."

cat > .doignore << EOF
# Archivos de desarrollo
*.pyc
__pycache__/
.pytest_cache/
.coverage
.env
.env.local
.env.development
.env.test
.env.production

# Archivos de IDE
.vscode/
.idea/
*.swp
*.swo

# Archivos de sistema
.DS_Store
Thumbs.db

# Archivos de logs
*.log
logs/

# Archivos temporales
tmp/
temp/

# Archivos de documentación
docs/
*.md
README.md

# Scripts de desarrollo
scripts/
tests/

# Archivos de configuración local
config/local.py
config/development.py
EOF

echo "✅ Archivo .doignore creado"

# Crear Procfile para compatibilidad
echo "📝 Creando Procfile..."

cat > backend/Procfile << EOF
web: uvicorn api.main:app --host 0.0.0.0 --port \$PORT
EOF

echo "✅ Procfile creado"

# Crear archivo de configuración de entorno
echo "📝 Creando archivo de configuración de entorno..."

cat > backend/.env.example << EOF
# Configuración de Gradient AI
DO_GRADIENT_INFERENCE_KEY=sk-do-tu-clave-aqui
GRADIENT_BASE_URL=https://inference.do-ai.run
GRADIENT_MODEL=openai-gpt-oss-120b

# Configuración de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-clave-anonima
SUPABASE_SERVICE_KEY=tu-clave-de-servicio

# Configuración de la aplicación
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=false
LOG_LEVEL=INFO

# Configuración de la base de datos
DATABASE_URL=postgresql://usuario:password@host:puerto/database
EOF

echo "✅ Archivo .env.example creado"

echo ""
echo "🎉 Configuración de despliegue completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Subir el código a GitHub"
echo "2. Crear la aplicación en DigitalOcean App Platform"
echo "3. Configurar las variables de entorno"
echo "4. Desplegar la aplicación"
echo ""
echo "🔗 Comandos útiles:"
echo "  - Verificar configuración: doctl apps create --spec .do/app.yaml --dry-run"
echo "  - Crear aplicación: doctl apps create --spec .do/app.yaml"
echo "  - Ver logs: doctl apps logs <app-id>"
echo ""
echo "📚 Documentación: https://docs.digitalocean.com/products/app-platform/"
