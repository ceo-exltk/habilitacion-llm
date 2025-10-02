"""
Configuración de la aplicación
"""

import os
from typing import Optional


class Settings:
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Habilitación LLM - Agentes Legales"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Configuración de Gradient AI
    DO_GRADIENT_INFERENCE_KEY: str = os.getenv("DO_GRADIENT_INFERENCE_KEY", "")
    GRADIENT_BASE_URL: str = os.getenv("GRADIENT_BASE_URL", "https://inference.do-ai.run")
    GRADIENT_MODEL: str = os.getenv("GRADIENT_MODEL", "openai-gpt-oss-120b")
    
    # Configuración de Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración de CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "https://legal-search-frontend-prod-wrvcg.ondigitalocean.app",
        "https://legal-search-frontend-staging-ooma3.ondigitalocean.app"
    ]
    
    # Configuración de la base de datos
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Configuración de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        """Validar configuración requerida"""
        if not self.DO_GRADIENT_INFERENCE_KEY:
            raise ValueError("DO_GRADIENT_INFERENCE_KEY es requerida")
        
        if not self.SUPABASE_URL:
            raise ValueError("SUPABASE_URL es requerida")
        
        if not self.SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_ANON_KEY es requerida")


# Instancia global de configuración
settings = Settings()
