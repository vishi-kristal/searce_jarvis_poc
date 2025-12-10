from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        # Exclude CORS_ORIGINS from Pydantic's automatic processing
        env_ignore_empty=True,
    )
    
    # Agent API Configuration
    AGENT_API_URL: str = os.getenv("AGENT_API_URL", "https://kristal-agent-953081186136.asia-southeast1.run.app")
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4")
    RELATIONSHIP_MANAGER_ID: str = os.getenv("RELATIONSHIP_MANAGER_ID", "001")
    
    # CORS Configuration - Read directly from env, don't let Pydantic process it
    @computed_field
    @property
    def CORS_ORIGINS(self) -> str:
        """Get CORS_ORIGINS directly from environment"""
        cors_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001")
        if not cors_env or cors_env.strip() == "":
            return "http://localhost:3000"
        return cors_env
    
    def get_cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        cors_str = self.CORS_ORIGINS
        if not cors_str or cors_str.strip() == "":
            return ["http://localhost:3000"]
        return [
            origin.strip() 
            for origin in cors_str.split(",")
            if origin.strip()
        ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

settings = Settings()

