from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SessionCreateSchema(BaseModel):
    clientId: str = Field(..., pattern=r'^K?\d+$', description="Client ID")
    kristalId: Optional[str] = Field(None, description="Optional Kristal ID")
    relationshipManagerId: Optional[str] = Field(None, description="Optional Relationship Manager ID")

class SessionResponseSchema(BaseModel):
    sessionId: str
    clientId: str
    kristalId: Optional[str]
    createdAt: datetime
    messageCount: int = 0

