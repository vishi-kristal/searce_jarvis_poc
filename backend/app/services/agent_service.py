import httpx
from typing import Optional
from app.config import settings
from app.utils.exceptions import AgentAPIError, NetworkError
from app.utils.logger import logger
from app.api.schemas.chat import ChatResponseSchema, SourceSchema, ValidationSchema, ChartSchema
import uuid
import re
import subprocess
import os

class AgentService:
    def __init__(self):
        self.base_url = settings.AGENT_API_URL
        self.api_key = settings.AGENT_API_KEY
        self.relationship_manager_id = settings.RELATIONSHIP_MANAGER_ID
        self.timeout = 300  # 5 minutes for long queries
    
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
    
    def _parse_sources_from_response(self, response_text: str) -> list:
        """Parse sources from agent response text (markdown format)"""
        sources = []
        # Look for source links in markdown format: [document name](url)
        source_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(source_pattern, response_text)
        
        for name, url in matches:
            source_type = "document"
            if "googleapis.com" in url or url.startswith("gs://"):
                source_type = "document"
            elif url.startswith("http"):
                source_type = "url"
            
            sources.append({
                "type": source_type,
                "name": name,
                "url": url
            })
        
        return sources
    
    def _parse_validation_from_response(self, response_text: str) -> Optional[dict]:
        """Parse validation results from agent response text"""
        # Look for validation section in the response
        validation_pattern = r'Validation Status[:\s]+(PASS|FAIL)'
        match = re.search(validation_pattern, response_text, re.IGNORECASE)
        
        if match:
            status = match.group(1).upper()
            # Try to extract summary and discrepancies
            summary_pattern = r'Summary of Findings[:\s]+([^\n]+)'
            summary_match = re.search(summary_pattern, response_text, re.IGNORECASE)
            summary = summary_match.group(1) if summary_match else ""
            
            # Extract discrepancies if FAIL
            discrepancies = []
            if status == "FAIL":
                disc_pattern = r'Discrepancies Found[:\s]+([^\n]+)'
                disc_match = re.search(disc_pattern, response_text, re.IGNORECASE)
                if disc_match:
                    discrepancies = [disc_match.group(1)]
            
            # Extract agent name
            agent_pattern = r'Agent ID Validated[:\s]+([^\n]+)'
            agent_match = re.search(agent_pattern, response_text, re.IGNORECASE)
            agent = agent_match.group(1).strip() if agent_match else "unknown"
            
            return {
                "status": status,
                "summary": summary,
                "discrepancies": discrepancies,
                "agent": agent
            }
        
        return None
    
    async def send_query(
        self,
        message: str,
        client_id: str,
        kristal_id: Optional[str] = None,
        session_id: Optional[str] = None,
        source: Optional[str] = None,
        relationship_manager_id: Optional[str] = None
    ) -> ChatResponseSchema:
        """
        Send query to agent API and return formatted response.
        
        API Endpoint: /query
        Request: { session_id, relationship_manager_id, client_id, kristal_id, query, source }
        Response: { agent_response, chart }
        """
        # Get authentication token (gcloud identity token or API key)
        auth_token = self._get_auth_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        # session_id is REQUIRED by the agent API
        if not session_id:
            raise AgentAPIError(
                "Session ID is required. Please create a session first.",
                status_code=400
            )
        
        # Prepare payload according to actual API specification
        payload = {
            "query": message,
            "client_id": client_id,
            "relationship_manager_id": relationship_manager_id or self.relationship_manager_id,
            "session_id": session_id,  # Required field
        }
        
        if kristal_id:
            payload["kristal_id"] = kristal_id
        
        if source:
            payload["source"] = source
        
        endpoint = f"{self.base_url}/query"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                logger.info(f"Calling agent API: {endpoint} with payload: {payload}")
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Extract agent_response and chart from response
                agent_response = data.get("agent_response", "")
                chart_data = data.get("chart")
                
                # Parse sources and validation from agent_response text
                sources = self._parse_sources_from_response(agent_response)
                validation = self._parse_validation_from_response(agent_response)
                
                # Handle chart if present
                chart = None
                if chart_data:
                    if isinstance(chart_data, dict):
                        chart = ChartSchema(**chart_data)
                    elif isinstance(chart_data, str):
                        # If chart is just a URL string
                        chart = ChartSchema(url=chart_data, title="Chart")
                
                return ChatResponseSchema(
                    response=agent_response,
                    sources=[SourceSchema(**s) for s in sources],
                    validation=ValidationSchema(**validation) if validation else None,
                    sessionId=session_id or str(uuid.uuid4()),
                    chart=chart,
                    metadata={"agent_api_response": data}
                )
                
            except httpx.HTTPStatusError as e:
                error_msg = f"Agent API error: {e.response.status_code}"
                logger.error(f"{error_msg} - Response: {e.response.text}")
                raise AgentAPIError(
                    error_msg,
                    status_code=e.response.status_code,
                    details=e.response.text
                )
            except httpx.TimeoutException:
                error_msg = "Agent API timeout"
                logger.error(error_msg)
                raise AgentAPIError(error_msg)
            except httpx.RequestError as e:
                error_msg = f"Network error: {str(e)}"
                logger.error(error_msg)
                raise NetworkError(error_msg, details=str(e))

