from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator
from typing import List, Any, Dict
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
    
    # CORS Configuration - Use string type, will be set in model_validator
    CORS_ORIGINS: str = ""
    
    @model_validator(mode='before')
    @classmethod
    def set_cors_origins(cls, data: Any) -> Dict[str, Any]:
        """Set CORS_ORIGINS from environment before Pydantic processes it"""
        if isinstance(data, dict):
            # Get CORS_ORIGINS directly from environment
            cors_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001")
            if not cors_env or cors_env.strip() == "":
                cors_env = "http://localhost:3000"
            data["CORS_ORIGINS"] = cors_env
        return data
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Any) -> str:
        """Parse CORS_ORIGINS - ensure it's always a string"""
        if v is None:
            return "http://localhost:3000"
        if isinstance(v, list):
            return ",".join(str(x) for x in v)
        if isinstance(v, str):
            if v.strip() == "":
                return "http://localhost:3000"
            return v
        return str(v) if v else "http://localhost:3000"
    
    def get_cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        if not self.CORS_ORIGINS or self.CORS_ORIGINS.strip() == "":
            return ["http://localhost:3000"]
        return [
            origin.strip() 
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

settings = Settings()

