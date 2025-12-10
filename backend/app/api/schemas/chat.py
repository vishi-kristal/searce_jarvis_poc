from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SourceSchema(BaseModel):
    type: str  # "document" | "table" | "url"
    name: str
    url: Optional[str] = None
    query: Optional[str] = None

class ValidationSchema(BaseModel):
    status: str  # "PASS" | "FAIL"
    summary: str
    discrepancies: List[str]
    agent: str

class ChartSchema(BaseModel):
    url: str
    title: str

class ChatRequestSchema(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="User query message")
    clientId: str = Field(..., pattern=r'^K?\d+$', description="Client ID (e.g., '16325000' or 'K16325000')")
    kristalId: Optional[str] = Field(None, description="Optional Kristal ID")
    sessionId: Optional[str] = Field(None, description="Optional session ID for conversation continuity")
    source: Optional[str] = Field(None, description="Optional source parameter")

class ChatResponseSchema(BaseModel):
    response: str
    sources: List[SourceSchema]
    validation: Optional[ValidationSchema] = None
    sessionId: str
    chart: Optional[ChartSchema] = None
    metadata: Optional[dict] = None

class ErrorResponseSchema(BaseModel):
    error: dict

