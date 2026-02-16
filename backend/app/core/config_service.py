import logging
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ApiKey
from app.core.security import security_service

logger = logging.getLogger(__name__)

class ConfigService:
    """Servicio centralizado para obtener configuración de API keys."""

    def __init__(self):
        pass

    async def get_active_api_key(self, provider: str = None) -> dict:
        """
        Obtiene la API key activa.

        Args:
            provider: Si se especifica, retorna la API key activa de ese proveedor.
                     Si es None, retorna la primera API key activa encontrada.

        Returns:
            Dict con: { 'api_key': str, 'model_preference': str, 'provider': str, 'key_id': int }
            o None si no hay API key activa.
        """
        try:
            db = next(get_db())

            # Construir query
            query = db.query(ApiKey).filter(ApiKey.is_active == 1)
            if provider:
                query = query.filter(ApiKey.provider == provider)

            active_key = query.first()

            if not active_key:
                logger.warning(f"No active API key found" + (f" for provider {provider}" if provider else ""))
                db.close()
                return None

            # Desencriptar la API key
            api_key_decrypted = security_service.decrypt_key(active_key.api_key_encrypted)

            # Actualizar contador de uso
            active_key.usage_count += 1
            from datetime import datetime
            active_key.last_used_at = datetime.utcnow()
            db.commit()

            db.close()

            return {
                'api_key': api_key_decrypted,
                'model_preference': active_key.model_preference,
                'provider': active_key.provider,
                'key_id': active_key.id,
                'usage_count': active_key.usage_count
            }

        except Exception as e:
            logger.error(f"Error getting active API key: {e}")
            return None

    async def get_all_active_providers(self) -> list:
        """
        Retorna lista de proveedores con al menos una API key activa.

        Returns:
            List de dicts: [{ 'provider': str, 'model_preference': str, 'usage_count': int }, ...]
        """
        try:
            db = next(get_db())

            active_keys = db.query(ApiKey).filter(ApiKey.is_active == 1).all()

            providers_info = []
            for key in active_keys:
                providers_info.append({
                    'provider': key.provider,
                    'model_preference': key.model_preference,
                    'usage_count': key.usage_count
                })

            db.close()

            return providers_info

        except Exception as e:
            logger.error(f"Error getting active providers: {e}")
            return []

    async def get_models_for_provider(self, provider: str) -> list:
        """
        Retorna lista de modelos disponibles para un proveedor.

        Args:
            provider: Nombre del proveedor (openai, anthropic, ollama)

        Returns:
            List de strings con nombres de modelos.
        """
        models = {
            "openai": ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            "ollama": ["llama3", "mistral", "gemma", "llama2"]
        }

        return models.get(provider, [])

# Singleton instance
config_service = ConfigService()

async def get_config_service() -> ConfigService:
    """Retorna la instancia singleton del servicio de configuración."""
    return config_service
