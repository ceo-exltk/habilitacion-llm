#!/usr/bin/env python3
"""
Script de prueba para la API de agentes LLM
"""

import asyncio
import httpx
import json
from typing import Dict, Any


class APITester:
    """Clase para probar la API de agentes LLM"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def test_health(self) -> Dict[str, Any]:
        """Prueba el endpoint de health"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_agent_health(self) -> Dict[str, Any]:
        """Prueba el endpoint de health del agente"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/agent/health")
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_create_user_config(self, user_id: str) -> Dict[str, Any]:
        """Prueba crear configuración de usuario"""
        try:
            config_data = {
                "user_id": user_id,
                "specialization": "penal",
                "tone": "formal",
                "temperature": 0.8,
                "max_tokens": 1500,
                "custom_instructions": "Eres un experto en derecho penal con 20 años de experiencia."
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/agent/config/{user_id}",
                json=config_data
            )
            
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_get_user_config(self, user_id: str) -> Dict[str, Any]:
        """Prueba obtener configuración de usuario"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/agent/config/{user_id}")
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_chat_with_agent(self, user_id: str, query: str) -> Dict[str, Any]:
        """Prueba chatear con el agente"""
        try:
            chat_data = {
                "query": query,
                "user_id": user_id,
                "context": "Consulta legal sobre derecho penal"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/agent/chat",
                json=chat_data
            )
            
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_get_models(self) -> Dict[str, Any]:
        """Prueba obtener modelos disponibles"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/agent/models")
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("🧪 Iniciando pruebas de la API de Agentes LLM")
        print("=" * 50)
        
        # Test 1: Health check
        print("\n1. Probando health check...")
        health_result = await self.test_health()
        print(f"   Status: {health_result['status']}")
        if health_result['status'] == 'success':
            print(f"   Response: {health_result['data']}")
        else:
            print(f"   Error: {health_result['error']}")
        
        # Test 2: Agent health
        print("\n2. Probando health del agente...")
        agent_health_result = await self.test_agent_health()
        print(f"   Status: {agent_health_result['status']}")
        if agent_health_result['status'] == 'success':
            print(f"   Response: {agent_health_result['data']}")
        else:
            print(f"   Error: {agent_health_result['error']}")
        
        # Test 3: Get models
        print("\n3. Probando obtener modelos...")
        models_result = await self.test_get_models()
        print(f"   Status: {models_result['status']}")
        if models_result['status'] == 'success':
            print(f"   Models: {models_result['data']}")
        else:
            print(f"   Error: {models_result['error']}")
        
        # Test 4: Create user config
        print("\n4. Probando crear configuración de usuario...")
        user_id = "test_user_123"
        create_result = await self.test_create_user_config(user_id)
        print(f"   Status: {create_result['status']}")
        if create_result['status'] == 'success':
            print(f"   Config creada: {create_result['data']}")
        else:
            print(f"   Error: {create_result['error']}")
        
        # Test 5: Get user config
        print("\n5. Probando obtener configuración de usuario...")
        get_config_result = await self.test_get_user_config(user_id)
        print(f"   Status: {get_config_result['status']}")
        if get_config_result['status'] == 'success':
            print(f"   Config obtenida: {get_config_result['data']}")
        else:
            print(f"   Error: {get_config_result['error']}")
        
        # Test 6: Chat with agent
        print("\n6. Probando chat con agente...")
        chat_result = await self.test_chat_with_agent(
            user_id, 
            "¿Cuáles son los elementos del delito de robo?"
        )
        print(f"   Status: {chat_result['status']}")
        if chat_result['status'] == 'success':
            print(f"   Respuesta del agente: {chat_result['data']['response'][:100]}...")
        else:
            print(f"   Error: {chat_result['error']}")
        
        print("\n" + "=" * 50)
        print("✅ Pruebas completadas")
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose()


async def main():
    """Función principal"""
    tester = APITester()
    try:
        await tester.run_all_tests()
    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())
