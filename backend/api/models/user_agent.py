"""
Modelos de datos para el sistema de personalización de agentes LLM
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class SpecializationType(str, Enum):
    """Tipos de especialización legal"""
    GENERAL = "general"
    PENAL = "penal"
    CIVIL = "civil"
    LABORAL = "laboral"


class ToneType(str, Enum):
    """Tipos de tono de comunicación"""
    FORMAL = "formal"
    COLOQUIAL = "coloquial"
    TECNICO = "tecnico"


class UserAgentConfig(BaseModel):
    """Configuración de agente por usuario"""
    user_id: str = Field(..., description="ID único del usuario")
    specialization: SpecializationType = Field(default=SpecializationType.GENERAL, description="Especialización legal")
    tone: ToneType = Field(default=ToneType.FORMAL, description="Tono de comunicación")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperatura del modelo (0.0-1.0)")
    model: str = Field(default="openai-gpt-oss-120b", description="Modelo LLM a utilizar")
    max_tokens: int = Field(default=1000, ge=1, le=4000, description="Máximo número de tokens")
    custom_instructions: Optional[str] = Field(default=None, description="Instrucciones personalizadas")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserAgentUpdate(BaseModel):
    """Modelo para actualizar configuración de agente"""
    specialization: Optional[SpecializationType] = None
    tone: Optional[ToneType] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0)
    model: Optional[str] = None
    max_tokens: Optional[int] = Field(None, ge=1, le=4000)
    custom_instructions: Optional[str] = None


class AgentResponse(BaseModel):
    """Respuesta del agente LLM"""
    response: str = Field(..., description="Respuesta generada por el agente")
    model_used: str = Field(..., description="Modelo utilizado para generar la respuesta")
    tokens_used: int = Field(..., description="Número de tokens utilizados")
    processing_time: float = Field(..., description="Tiempo de procesamiento en segundos")
    user_config: UserAgentConfig = Field(..., description="Configuración del usuario utilizada")


class SearchRequest(BaseModel):
    """Solicitud de búsqueda legal"""
    query: str = Field(..., description="Consulta legal")
    user_id: str = Field(..., description="ID del usuario")
    context: Optional[str] = Field(default=None, description="Contexto adicional")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filtros de búsqueda")


class SearchResponse(BaseModel):
    """Respuesta de búsqueda legal"""
    results: list = Field(..., description="Resultados de la búsqueda")
    total_results: int = Field(..., description="Total de resultados encontrados")
    query: str = Field(..., description="Consulta original")
    processing_time: float = Field(..., description="Tiempo de procesamiento")
    user_config: UserAgentConfig = Field(..., description="Configuración del usuario")
