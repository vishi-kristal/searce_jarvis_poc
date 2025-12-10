from fastapi import APIRouter
from datetime import datetime
from app.services.agent_service import AgentService
from app.utils.logger import logger
from app.config import settings

router = APIRouter()
agent_service = AgentService()

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns the health status of the API and agent service.
    """
    try:
        # Check agent API availability (simple check)
        agent_api_status = "available"
        try:
            # You can add a simple ping/health check to agent API here
            # For now, we'll assume it's available
            pass
        except Exception:
            agent_api_status = "unavailable"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "agentApiStatus": agent_api_status,
            "cors_origins": settings.get_cors_origins_list(),
            "cors_origins_count": len(settings.get_cors_origins_list())
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

