"""
Servicio para gestionar configuraciones de agentes por usuario
"""

import json
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.user_agent import UserAgentConfig, UserAgentUpdate, SpecializationType, ToneType


class UserAgentService:
    """Servicio para gestionar configuraciones de agentes por usuario"""
    
    def __init__(self):
        # En producción, esto debería ser una base de datos
        # Por ahora usamos un diccionario en memoria
        self._user_configs: Dict[str, UserAgentConfig] = {}
    
    def get_user_config(self, user_id: str) -> Optional[UserAgentConfig]:
        """
        Obtiene la configuración de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            UserAgentConfig o None si no existe
        """
        return self._user_configs.get(user_id)
    
    def create_user_config(self, user_id: str, config: UserAgentConfig) -> UserAgentConfig:
        """
        Crea una nueva configuración para un usuario
        
        Args:
            user_id: ID del usuario
            config: Configuración del agente
            
        Returns:
            UserAgentConfig creada
        """
        config.user_id = user_id
        config.created_at = datetime.utcnow()
        config.updated_at = datetime.utcnow()
        
        self._user_configs[user_id] = config
        return config
    
    def update_user_config(self, user_id: str, update_data: UserAgentUpdate) -> Optional[UserAgentConfig]:
        """
        Actualiza la configuración de un usuario
        
        Args:
            user_id: ID del usuario
            update_data: Datos a actualizar
            
        Returns:
            UserAgentConfig actualizada o None si no existe
        """
        existing_config = self._user_configs.get(user_id)
        if not existing_config:
            return None
        
        # Actualizar solo los campos proporcionados
        update_dict = update_data.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            if hasattr(existing_config, field):
                setattr(existing_config, field, value)
        
        existing_config.updated_at = datetime.utcnow()
        
        return existing_config
    
    def delete_user_config(self, user_id: str) -> bool:
        """
        Elimina la configuración de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si se eliminó, False si no existía
        """
        if user_id in self._user_configs:
            del self._user_configs[user_id]
            return True
        return False
    
    def get_default_config(self, user_id: str) -> UserAgentConfig:
        """
        Obtiene la configuración por defecto para un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            UserAgentConfig con valores por defecto
        """
        return UserAgentConfig(
            user_id=user_id,
            specialization=SpecializationType.GENERAL,
            tone=ToneType.FORMAL,
            temperature=0.7,
            model="openai-gpt-oss-120b",
            max_tokens=32000
        )
    
    def get_or_create_user_config(self, user_id: str) -> UserAgentConfig:
        """
        Obtiene la configuración de un usuario o crea una por defecto
        
        Args:
            user_id: ID del usuario
            
        Returns:
            UserAgentConfig existente o nueva
        """
        existing_config = self.get_user_config(user_id)
        if existing_config:
            return existing_config
        
        # Crear configuración por defecto
        default_config = self.get_default_config(user_id)
        return self.create_user_config(user_id, default_config)
    
    def get_all_user_configs(self) -> Dict[str, UserAgentConfig]:
        """
        Obtiene todas las configuraciones de usuarios
        
        Returns:
            Diccionario con todas las configuraciones
        """
        return self._user_configs.copy()
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con estadísticas
        """
        config = self.get_user_config(user_id)
        if not config:
            return {"error": "Usuario no encontrado"}
        
        return {
            "user_id": user_id,
            "specialization": config.specialization.value,
            "tone": config.tone.value,
            "temperature": config.temperature,
            "model": config.model,
            "max_tokens": config.max_tokens,
            "has_custom_instructions": bool(config.custom_instructions),
            "created_at": config.created_at.isoformat(),
            "updated_at": config.updated_at.isoformat()
        }
    
    def export_user_config(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Exporta la configuración de un usuario en formato JSON
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con la configuración o None si no existe
        """
        config = self.get_user_config(user_id)
        if not config:
            return None
        
        return {
            "user_id": config.user_id,
            "specialization": config.specialization.value,
            "tone": config.tone.value,
            "temperature": config.temperature,
            "model": config.model,
            "max_tokens": config.max_tokens,
            "custom_instructions": config.custom_instructions,
            "created_at": config.created_at.isoformat(),
            "updated_at": config.updated_at.isoformat()
        }
    
    def import_user_config(self, config_data: Dict[str, Any]) -> Optional[UserAgentConfig]:
        """
        Importa una configuración de usuario desde un diccionario
        
        Args:
            config_data: Datos de configuración
            
        Returns:
            UserAgentConfig importada o None si hay error
        """
        try:
            # Validar campos requeridos
            if "user_id" not in config_data:
                return None
            
            # Crear configuración
            config = UserAgentConfig(
                user_id=config_data["user_id"],
                specialization=SpecializationType(config_data.get("specialization", "general")),
                tone=ToneType(config_data.get("tone", "formal")),
                temperature=config_data.get("temperature", 0.7),
                model=config_data.get("model", "openai-gpt-oss-120b"),
                max_tokens=config_data.get("max_tokens", 32000),
                custom_instructions=config_data.get("custom_instructions")
            )
            
            # Actualizar timestamps si están en los datos
            if "created_at" in config_data:
                config.created_at = datetime.fromisoformat(config_data["created_at"])
            if "updated_at" in config_data:
                config.updated_at = datetime.fromisoformat(config_data["updated_at"])
            
            # Guardar configuración
            self._user_configs[config.user_id] = config
            return config
            
        except Exception as e:
            print(f"Error importando configuración: {e}")
            return None
