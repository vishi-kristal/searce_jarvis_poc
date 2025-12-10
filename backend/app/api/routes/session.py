from fastapi import APIRouter, HTTPException
from app.api.schemas.session import SessionCreateSchema, SessionResponseSchema
from app.services.session_service import SessionService
from app.utils.logger import logger
import uuid
from datetime import datetime

router = APIRouter()
session_service = SessionService()

@router.post("/session", response_model=SessionResponseSchema)
async def create_session(request: SessionCreateSchema):
    """
    Create a new session via the agent API.
    
    - **clientId**: Client ID (e.g., "16325000" or "K16325000")
    - **kristalId**: Optional Kristal ID
    - **relationshipManagerId**: Optional Relationship Manager ID (defaults to config value)
    """
    try:
        # Normalize client ID
        normalized_client_id = request.clientId.lstrip('K')
        
        # Create session via agent API
        session_id = await session_service.create_session_via_api(
            client_id=normalized_client_id,
            kristal_id=request.kristalId,
            relationship_manager_id=request.relationshipManagerId
        )
        
        # Get session data from local cache
        session_data = session_service.get_session(session_id)
        
        if not session_data:
            raise HTTPException(status_code=500, detail="Session created but not found in cache")
        
        logger.info(f"Created session {session_id} for clientId: {normalized_client_id}")
        
        return SessionResponseSchema(
            sessionId=session_data["sessionId"],
            clientId=session_data["clientId"],
            kristalId=session_data.get("kristalId"),
            createdAt=session_data["createdAt"],
            messageCount=session_data.get("messageCount", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

@router.get("/session/{session_id}", response_model=SessionResponseSchema)
async def get_session(session_id: str):
    """Get session details by session ID"""
    try:
        session_data = session_service.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionResponseSchema(**session_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session")

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    try:
        success = session_service.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        logger.info(f"Deleted session {session_id}")
        return {"success": True, "message": "Session deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

