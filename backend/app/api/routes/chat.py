from fastapi import APIRouter, HTTPException
from app.api.schemas.chat import ChatRequestSchema, ChatResponseSchema, ErrorResponseSchema
from app.services.agent_service import AgentService
from app.services.session_service import SessionService
from app.config import settings
from app.utils.logger import logger

router = APIRouter()
agent_service = AgentService()
session_service = SessionService()

@router.post(
    "/chat",
    response_model=ChatResponseSchema,
    responses={502: {"model": ErrorResponseSchema}, 503: {"model": ErrorResponseSchema}}
)
async def send_chat_message(request: ChatRequestSchema):
    """
    Send a chat message to the agent and receive a response.
    
    - **message**: User's query/question
    - **clientId**: Client ID (e.g., "16325000" or "K16325000")
    - **kristalId**: Optional Kristal ID
    - **sessionId**: Optional session ID for conversation continuity
    - **source**: Optional source parameter
    """
    try:
        logger.info(f"Received chat request for clientId: {request.clientId}")
        
        # Normalize client ID (remove K prefix if present)
        normalized_client_id = request.clientId.lstrip('K')
        
        # Auto-create session if not provided (session_id is required by agent API)
        session_id = request.sessionId
        if not session_id:
            try:
                logger.info(f"Auto-creating session for clientId: {normalized_client_id}")
                session_id = await session_service.create_session_via_api(
                    client_id=normalized_client_id,
                    kristal_id=request.kristalId
                )
                logger.info(f"Auto-created session: {session_id}")
            except Exception as e:
                logger.error(f"Failed to auto-create session: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": {
                            "code": "SESSION_CREATION_ERROR",
                            "message": "Failed to create session. Please create a session first.",
                            "details": str(e)
                        }
                    }
                )
        
        # Call agent service
        response = await agent_service.send_query(
            message=request.message,
            client_id=normalized_client_id,
            kristal_id=request.kristalId,
            session_id=session_id,
            source=request.source,
            relationship_manager_id=settings.RELATIONSHIP_MANAGER_ID
        )
        
        logger.info(f"Successfully received response from agent API")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Failed to process chat request",
                    "details": str(e)
                }
            }
        )

