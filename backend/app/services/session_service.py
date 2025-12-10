from typing import Optional, Dict
from datetime import datetime, timedelta
from app.config import settings
from app.utils.logger import logger
from app.utils.exceptions import AgentAPIError, NetworkError
import httpx
import subprocess

class SessionService:
    """
    Session management service.
    
    Creates sessions via the agent API /get_session endpoint.
    Also maintains local cache for session metadata.
    """
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.timeout_minutes = settings.SESSION_TIMEOUT_MINUTES
        self.base_url = settings.AGENT_API_URL
        self.api_key = settings.AGENT_API_KEY
        self.relationship_manager_id = settings.RELATIONSHIP_MANAGER_ID
    
    def _get_auth_token(self) -> str:
        """
        Get authentication token for agent API.
        Tries gcloud identity token first, falls back to API key.
        """
        # Try to get gcloud identity token (for local development with gcloud CLI)
        try:
            result = subprocess.run(
                ['gcloud', 'auth', 'print-identity-token'],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            token = result.stdout.strip()
            if token:
                logger.info("Using gcloud identity token for authentication")
                return token
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # Fall back to API key if gcloud is not available
            logger.info("gcloud not available, using API key")
            pass
        
        # Fallback to API key
        return self.api_key
    
    async def create_session_via_api(
        self,
        client_id: str,
        kristal_id: Optional[str] = None,
        relationship_manager_id: Optional[str] = None
    ) -> str:
        """
        Create a session via the agent API /get_session endpoint.
        Returns the session_id from the API.
        """
        # Get authentication token (gcloud identity token or API key)
        auth_token = self._get_auth_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        payload = {
            "client_id": client_id,
            "relationship_manager_id": relationship_manager_id or self.relationship_manager_id,
        }
        
        if kristal_id:
            payload["kristal_id"] = kristal_id
        
        endpoint = f"{self.base_url}/get_session"
        
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                logger.info(f"Creating session via API: {endpoint}")
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                response.raise_for_status()
                data = response.json()
                
                session_id = data.get("session_id")
                if not session_id:
                    raise AgentAPIError("No session_id in API response")
                
                # Store session metadata locally
                session_data = {
                    "sessionId": session_id,
                    "clientId": client_id,
                    "kristalId": kristal_id,
                    "createdAt": datetime.now(),
                    "messageCount": 0
                }
                self.create_session(session_id, session_data)
                
                logger.info(f"Created session {session_id} via API for clientId: {client_id}")
                return session_id
                
            except httpx.HTTPStatusError as e:
                error_msg = f"Agent API error creating session: {e.response.status_code}"
                logger.error(f"{error_msg} - Response: {e.response.text}")
                raise AgentAPIError(
                    error_msg,
                    status_code=e.response.status_code,
                    details=e.response.text
                )
            except httpx.RequestError as e:
                error_msg = f"Network error creating session: {str(e)}"
                logger.error(error_msg)
                raise NetworkError(error_msg, details=str(e))
    
    def create_session(self, session_id: str, session_data: Dict) -> None:
        """Create a new session"""
        self.sessions[session_id] = session_data
        logger.info(f"Created session: {session_id}")
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        # Check if session has expired
        created_at = session.get("createdAt")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        if isinstance(created_at, datetime):
            if datetime.now() - created_at > timedelta(minutes=self.timeout_minutes):
                logger.info(f"Session {session_id} expired")
                del self.sessions[session_id]
                return None
        
        return session
    
    def update_session(self, session_id: str, updates: Dict) -> bool:
        """Update session data"""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id].update(updates)
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        now = datetime.now()
        expired = []
        
        for session_id, session_data in self.sessions.items():
            created_at = session_data.get("createdAt")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            if isinstance(created_at, datetime):
                if now - created_at > timedelta(minutes=self.timeout_minutes):
                    expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
        
        return len(expired)

