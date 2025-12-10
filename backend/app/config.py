from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

def _get_cors_origins_from_env() -> str:
    """
    Get CORS_ORIGINS directly from environment, bypassing Pydantic.
    
    IMPORTANT: In production (Railways), you MUST set CORS_ORIGINS environment variable
    with your Vercel frontend URL, e.g.:
    CORS_ORIGINS=https://searce-jarvis-poc.vercel.app,http://localhost:3000
    
    Default is only for local development.
    """
    cors_env = os.getenv("CORS_ORIGINS")
    if not cors_env or cors_env.strip() == "":
        # Default only for local development
        # In production, CORS_ORIGINS MUST be set via environment variable
        return "http://localhost:3000,http://localhost:3001"
    return cors_env

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )
    
    # Agent API Configuration
    AGENT_API_URL: str = os.getenv("AGENT_API_URL", "https://kristal-agent-953081186136.asia-southeast1.run.app")
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4")
    RELATIONSHIP_MANAGER_ID: str = os.getenv("RELATIONSHIP_MANAGER_ID", "001")
    
    # Note: CORS_ORIGINS is NOT a Pydantic field - we read it directly
    # This prevents Pydantic from trying to parse it as JSON
    
    def get_cors_origins_list(self) -> List[str]:
        """
        Get CORS origins as a list - reads directly from environment.
        
        IMPORTANT: In production, set CORS_ORIGINS environment variable in Railways
        with your Vercel frontend URL.
        """
        cors_str = _get_cors_origins_from_env()
        if not cors_str or cors_str.strip() == "":
            # Fallback for local development only
            return ["http://localhost:3000"]
        return [
            origin.strip() 
            for origin in cors_str.split(",")
            if origin.strip()
        ]
    
    @property
    def CORS_ORIGINS(self) -> str:
        """Get CORS_ORIGINS as string - reads directly from environment"""
        return _get_cors_origins_from_env()
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

settings = Settings()

