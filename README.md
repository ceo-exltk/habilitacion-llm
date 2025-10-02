# 🤖 Habilitación LLM - Sistema de Agentes Legales Personalizables

## 📋 Descripción del Proyecto

Sistema de agentes legales personalizables que permite a los usuarios configurar y personalizar el comportamiento de agentes LLM para consultas legales específicas.

## 🏗️ Arquitectura

### FASE 0: MVP con Gradient AI Platform
- **Backend:** Python FastAPI
- **Frontend:** Next.js
- **LLM:** DigitalOcean Gradient AI Platform
- **Base de Datos:** Supabase
- **Despliegue:** DigitalOcean App Platform

### Configuración Actual
- **Modelo:** `openai-gpt-oss-120b`
- **Endpoint:** `https://inference.do-ai.run`
- **API Key:** Configurada en variables de entorno

## 🚀 Funcionalidades

### FASE 0: Personalización Básica
- [x] Configuración de especialización (General, Penal, Civil, Laboral)
- [x] Configuración de tono (Formal, Coloquial, Técnico)
- [x] Configuración de temperatura (0.0 - 1.0)
- [x] Persistencia de configuraciones por usuario
- [x] API de personalización

### FASE 1: Arquitectura Avanzada
- [ ] Sistema de configuración por archivos
- [ ] Panel de personalización avanzado
- [ ] Integración profunda con Supabase
- [ ] Sistema de detección de pantalla inteligente

### FASE 2: Optimización y Migración
- [ ] Sistema de A/B testing
- [ ] Monitoreo avanzado
- [ ] Migración a modelos privados
- [ ] Documentación completa

## 📁 Estructura del Proyecto

```
habilitacion_llm/
├── backend/                 # API FastAPI
│   ├── api/
│   │   ├── endpoints/       # Endpoints de la API
│   │   ├── models/         # Modelos de datos
│   │   └── services/       # Servicios de negocio
│   ├── config/             # Configuración
│   └── requirements.txt
├── frontend/               # Aplicación Next.js
│   ├── components/         # Componentes React
│   ├── pages/             # Páginas
│   └── styles/            # Estilos
├── docs/                  # Documentación
└── scripts/               # Scripts de despliegue
```

## 🔧 Configuración

### Variables de Entorno
```bash
# Gradient AI Platform
DO_GRADIENT_INFERENCE_KEY=sk-do-tMbhJd4J9lY7wtTTVgpwL4uyQNIPcf34v5w5vqLrM2woXbH5Z1Z_SOQDld
GRADIENT_BASE_URL=https://inference.do-ai.run
GRADIENT_MODEL=openai-gpt-oss-120b

# Supabase
SUPABASE_URL=https://arixuftpeoplurjavqnb.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=EV[1:tKFaiXTcwxser9LqgxFu8crSBQjYmSKW...]

# Aplicación
SECRET_KEY=your-super-secret-jwt-key-here
DEBUG=false
```

## 🚀 Despliegue

### Desarrollo Local
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Producción
- **Backend:** DigitalOcean App Platform
- **Frontend:** DigitalOcean App Platform
- **Base de Datos:** Supabase

## 📊 Estado del Proyecto

- **FASE 0:** En desarrollo
- **FASE 1:** Pendiente
- **FASE 2:** Pendiente

## 🔗 Enlaces Útiles

- [DigitalOcean Gradient AI Platform](https://cloud.digitalocean.com/gen-ai)
- [Supabase Dashboard](https://supabase.com/dashboard)
- [Documentación de la API](https://legal-semantic-search-staging-f8pwz.ondigitalocean.app/legal-semantic-search2/docs)
