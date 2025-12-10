from fastapi import APIRouter
from app.config import settings
import os

router = APIRouter()

@router.get("/debug/env")
async def debug_env():
    """
    Debug endpoint to check environment variables.
    Shows what the backend is actually reading.
    """
    return {
        "raw_cors_origins_env": os.getenv("CORS_ORIGINS", "NOT SET"),
        "parsed_cors_origins": settings.get_cors_origins_list(),
        "cors_origins_count": len(settings.get_cors_origins_list()),
        "agent_api_url": settings.AGENT_API_URL,
        "relationship_manager_id": settings.RELATIONSHIP_MANAGER_ID,
        "environment": settings.ENVIRONMENT,
        "all_env_vars": {
            "CORS_ORIGINS": os.getenv("CORS_ORIGINS", "NOT SET"),
            "AGENT_API_URL": os.getenv("AGENT_API_URL", "NOT SET"),
            "RELATIONSHIP_MANAGER_ID": os.getenv("RELATIONSHIP_MANAGER_ID", "NOT SET"),
        }
    }

