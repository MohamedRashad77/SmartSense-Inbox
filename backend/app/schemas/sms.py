from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Request schemas
class SMSIngest(BaseModel):
    sender: str
    body: str
    timestamp: Optional[datetime] = None
    message_id: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    date: Optional[str] = None

# Response schemas
class SMSResponse(BaseModel):
    id: int
    sender: str
    body: str
    timestamp: datetime
    category: Optional[str] = None
    is_threat: bool = False
    threat_reason: Optional[str] = None
    urls: Optional[List[str]] = None
    has_money_request: bool = False
    has_otp: bool = False
    
    class Config:
        from_attributes = True

class CategoryDigest(BaseModel):
    category: str
    count: int
    summary: str

class DigestResponse(BaseModel):
    date: str
    total_messages: int
    categories: List[CategoryDigest]
    threat_count: int

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[int]] = None  # message IDs