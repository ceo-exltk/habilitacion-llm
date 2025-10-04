"""
Servicio para interactuar con DigitalOcean Gradient AI Platform
"""

import os
import time
import httpx
from typing import Dict, Any, Optional
from ..models.user_agent import UserAgentConfig, AgentResponse


class GradientAIService:
    """Servicio para interactuar con Gradient AI Platform"""
    
    def __init__(self):
        self.api_key = os.getenv("DO_GRADIENT_INFERENCE_KEY")
        self.base_url = os.getenv("GRADIENT_BASE_URL", "https://inference.do-ai.run")
        self.model = os.getenv("GRADIENT_MODEL", "openai-gpt-oss-120b")
        
        # Para desarrollo, usar valores por defecto si no están configurados
        if not self.api_key:
            self.api_key = "sk-do-tMbhJd4J9lY7wtTTVgpwL4uyQNIPcf34v5w5vqLrM2woXbH5Z1Z_SOQDld"
            print("⚠️  Usando API key por defecto para desarrollo")
    
    async def generate_response(
        self, 
        prompt: str, 
        user_config: UserAgentConfig,
        context: Optional[str] = None
    ) -> AgentResponse:
        """
        Genera una respuesta usando Gradient AI Platform
        
        Args:
            prompt: Prompt del usuario
            user_config: Configuración del usuario
            context: Contexto adicional opcional
            
        Returns:
            AgentResponse: Respuesta generada por el agente
        """
        start_time = time.time()
        
        # Construir el prompt completo con la configuración del usuario
        full_prompt = self._build_prompt(prompt, user_config, context)
        
        # Preparar la solicitud
        request_data = {
            "model": user_config.model,
            "messages": [
                {
                    "role": "system",
                    "content": self._build_system_prompt(user_config)
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "temperature": user_config.temperature,
            "max_tokens": user_config.max_tokens,
            "stream": False
        }
        
        # Realizar la solicitud
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=request_data,
                timeout=120.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Error en Gradient AI: {response.status_code} - {response.text}")
            
            result = response.json()
        
        processing_time = time.time() - start_time
        
        return AgentResponse(
            response=result["choices"][0]["message"]["content"],
            model_used=user_config.model,
            tokens_used=result["usage"]["total_tokens"],
            processing_time=processing_time,
            user_config=user_config
        )
    
    def _build_system_prompt(self, user_config: UserAgentConfig) -> str:
        """Construye el prompt del sistema basado en la configuración del usuario"""
        
        # Prompt base del agente legal
        base_prompt = """Eres un asistente legal especializado que ayuda con consultas jurídicas. 
        Tu objetivo es proporcionar información legal precisa, útil y comprensible."""
        
        # Agregar especialización
        specialization_prompts = {
            "general": "Tienes conocimientos generales en derecho y puedes ayudar con consultas de diversas áreas legales.",
            "penal": "Te especializas en derecho penal y puedes ayudar con consultas sobre delitos, procedimientos penales y defensa criminal.",
            "civil": "Te especializas en derecho civil y puedes ayudar con consultas sobre contratos, responsabilidad civil, familia y sucesiones.",
            "laboral": "Te especializas en derecho laboral y puedes ayudar con consultas sobre relaciones laborales, derechos del trabajador y empleador."
        }
        
        specialization_prompt = specialization_prompts.get(user_config.specialization.value, specialization_prompts["general"])
        
        # Agregar tono
        tone_prompts = {
            "formal": "Utiliza un lenguaje formal y técnico, apropiado para documentos legales y comunicaciones oficiales.",
            "coloquial": "Utiliza un lenguaje claro y accesible, explicando conceptos legales de manera sencilla.",
            "tecnico": "Utiliza terminología legal precisa y técnica, apropiada para profesionales del derecho."
        }
        
        tone_prompt = tone_prompts.get(user_config.tone.value, tone_prompts["formal"])
        
        # Agregar instrucciones personalizadas si existen
        custom_instructions = ""
        if user_config.custom_instructions:
            custom_instructions = f"\n\nInstrucciones personalizadas: {user_config.custom_instructions}"
        
        return f"{base_prompt}\n\n{specialization_prompt}\n\n{tone_prompt}{custom_instructions}"
    
    def _build_prompt(self, user_prompt: str, user_config: UserAgentConfig, context: Optional[str] = None) -> str:
        """Construye el prompt completo del usuario"""
        
        prompt_parts = [user_prompt]
        
        if context:
            prompt_parts.insert(0, f"Contexto: {context}")
        
        return "\n\n".join(prompt_parts)
    
    async def test_connection(self) -> Dict[str, Any]:
        """Prueba la conexión con Gradient AI Platform"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": "Test"}],
                        "max_tokens": 50
                    },
                    timeout=10.0
                )
                
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "model": self.model,
                    "base_url": self.base_url
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model,
                "base_url": self.base_url
            }
