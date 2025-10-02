# Habilitación de Agentes LLM

Sistema de agentes legales personalizables con LLM - Habilitación de Agentes LLM

## Descripción

Este proyecto implementa un sistema de agentes legales personalizables utilizando modelos de lenguaje (LLM) a través de DigitalOcean Gradient AI Platform.

## Características

- Integración con DigitalOcean Gradient AI Platform
- Modelos LLM locales para privacidad
- Sistema de personalización por usuario
- API REST con FastAPI
- Despliegue automático con GitHub Actions

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/ceo-exltk/habilitacion-llm.git
cd habilitacion-llm

# Instalar dependencias
cd backend
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales

# Ejecutar la aplicación
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Uso

La API estará disponible en `http://localhost:8000` con documentación automática en `http://localhost:8000/docs`.

## Despliegue

El proyecto se despliega automáticamente en DigitalOcean App Platform mediante GitHub Actions.

## Licencia

Este proyecto es privado y confidencial.
