from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )
    
    # Agent API Configuration
    AGENT_API_URL: str = os.getenv("AGENT_API_URL", "https://kristal-agent-953081186136.asia-southeast1.run.app")
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4")
    RELATIONSHIP_MANAGER_ID: str = os.getenv("RELATIONSHIP_MANAGER_ID", "001")
    
    # CORS Configuration - Don't let Pydantic process this, read directly
    # We'll use a property to access it
    _cors_origins: str = ""
    
    def __init__(self, **kwargs):
        # Read CORS_ORIGINS directly from environment, bypassing Pydantic
        cors_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001")
        if not cors_env or cors_env.strip() == "":
            cors_env = "http://localhost:3000"
        self._cors_origins = cors_env
        # Don't pass CORS_ORIGINS to Pydantic
        kwargs.pop("CORS_ORIGINS", None)
        super().__init__(**kwargs)
    
    @property
    def CORS_ORIGINS(self) -> str:
        """Get CORS_ORIGINS as string"""
        return self._cors_origins
    
    def get_cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        if not self._cors_origins or self._cors_origins.strip() == "":
            return ["http://localhost:3000"]
        return [
            origin.strip() 
            for origin in self._cors_origins.split(",")
            if origin.strip()
        ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

settings = Settings()

