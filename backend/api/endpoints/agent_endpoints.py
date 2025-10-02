"""
Endpoints para el sistema de agentes LLM personalizables
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..models.user_agent import (
    UserAgentConfig, 
    UserAgentUpdate, 
    AgentResponse, 
    SearchRequest, 
    SearchResponse
)
from ..services.user_agent_service import UserAgentService
from ..services.gradient_service import GradientAIService

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])

# Instancias de servicios
user_service = UserAgentService()
gradient_service = GradientAIService()


@router.get("/config/{user_id}", response_model=UserAgentConfig)
async def get_user_config(user_id: str):
    """
    Obtiene la configuración de un usuario
    """
    config = user_service.get_or_create_user_config(user_id)
    return config


@router.put("/config/{user_id}", response_model=UserAgentConfig)
async def update_user_config(user_id: str, update_data: UserAgentUpdate):
    """
    Actualiza la configuración de un usuario
    """
    config = user_service.update_user_config(user_id, update_data)
    if not config:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return config


@router.post("/config/{user_id}", response_model=UserAgentConfig)
async def create_user_config(user_id: str, config: UserAgentConfig):
    """
    Crea una nueva configuración para un usuario
    """
    existing_config = user_service.get_user_config(user_id)
    if existing_config:
        raise HTTPException(status_code=409, detail="La configuración ya existe")
    
    new_config = user_service.create_user_config(user_id, config)
    return new_config


@router.delete("/config/{user_id}")
async def delete_user_config(user_id: str):
    """
    Elimina la configuración de un usuario
    """
    success = user_service.delete_user_config(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": "Configuración eliminada exitosamente"}


@router.get("/config/{user_id}/stats")
async def get_user_stats(user_id: str):
    """
    Obtiene estadísticas de un usuario
    """
    stats = user_service.get_user_stats(user_id)
    if "error" in stats:
        raise HTTPException(status_code=404, detail=stats["error"])
    return stats


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: SearchRequest):
    """
    Chatea con el agente LLM usando la configuración del usuario
    """
    # Obtener configuración del usuario
    user_config = user_service.get_or_create_user_config(request.user_id)
    
    # Generar respuesta usando Gradient AI
    try:
        response = await gradient_service.generate_response(
            prompt=request.query,
            user_config=user_config,
            context=request.context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")


@router.post("/search", response_model=SearchResponse)
async def search_legal_documents(request: SearchRequest):
    """
    Busca documentos legales usando la configuración del usuario
    """
    # Obtener configuración del usuario
    user_config = user_service.get_or_create_user_config(request.user_id)
    
    # Aquí integrarías con Supabase para búsqueda real
    # Por ahora retornamos un mock
    mock_results = [
        {
            "title": "Documento legal de ejemplo",
            "content": "Contenido del documento...",
            "relevance_score": 0.95,
            "source": "Base de datos legal"
        }
    ]
    
    return SearchResponse(
        results=mock_results,
        total_results=len(mock_results),
        query=request.query,
        processing_time=0.5,
        user_config=user_config
    )


@router.get("/health")
async def health_check():
    """
    Verifica el estado del servicio
    """
    try:
        # Probar conexión con Gradient AI
        connection_test = await gradient_service.test_connection()
        
        return {
            "status": "healthy",
            "gradient_ai": connection_test,
            "user_configs_count": len(user_service.get_all_user_configs())
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/models")
async def get_available_models():
    """
    Obtiene los modelos disponibles
    """
    return {
        "models": [
            {
                "id": "openai-gpt-oss-120b",
                "name": "OpenAI GPT OSS 120B",
                "description": "Modelo de 120B parámetros optimizado para tareas legales",
                "max_tokens": 4000,
                "supports_streaming": True
            }
        ],
        "current_model": "openai-gpt-oss-120b"
    }


@router.get("/specializations")
async def get_specializations():
    """
    Obtiene las especializaciones disponibles
    """
    return {
        "specializations": [
            {
                "id": "general",
                "name": "General",
                "description": "Conocimientos generales en derecho"
            },
            {
                "id": "penal",
                "name": "Penal",
                "description": "Especialización en derecho penal"
            },
            {
                "id": "civil",
                "name": "Civil",
                "description": "Especialización en derecho civil"
            },
            {
                "id": "laboral",
                "name": "Laboral",
                "description": "Especialización en derecho laboral"
            }
        ]
    }


@router.get("/tones")
async def get_tones():
    """
    Obtiene los tonos disponibles
    """
    return {
        "tones": [
            {
                "id": "formal",
                "name": "Formal",
                "description": "Lenguaje formal y técnico"
            },
            {
                "id": "coloquial",
                "name": "Coloquial",
                "description": "Lenguaje claro y accesible"
            },
            {
                "id": "tecnico",
                "name": "Técnico",
                "description": "Terminología legal precisa"
            }
        ]
    }
