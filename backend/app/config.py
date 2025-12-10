from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Agent API Configuration
    AGENT_API_URL: str = os.getenv("AGENT_API_URL", "https://kristal-agent-953081186136.asia-southeast1.run.app")
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4")
    RELATIONSHIP_MANAGER_ID: str = os.getenv("RELATIONSHIP_MANAGER_ID", "001")
    
    # CORS Configuration - Use string type to avoid JSON parsing issues
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001")
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> str:
        """Parse CORS_ORIGINS - keep as string for Pydantic, parse later"""
        if isinstance(v, list):
            return ",".join(v)
        if not v or v.strip() == "":
            return "http://localhost:3000"
        return v
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

