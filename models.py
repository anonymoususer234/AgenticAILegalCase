from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class LegalQuery(BaseModel):
    query: str
    jurisdiction: Optional[str] = None
    case_types: Optional[List[str]] = None

class Citation(BaseModel):
    case_name: str
    citation: str
    court: str
    date: datetime
    jurisdiction: str
    relevance_score: float
    url: Optional[str] = None

class LegalFinding(BaseModel):
    content: str
    source: str
    citations: List[Citation]
    relevance_score: float
    authority_score: float

class LegalBrief(BaseModel):
    query: str
    executive_summary: str
    key_findings: List[str]
    supporting_cases: List[Citation]
    legal_analysis: str
    conclusions: List[str]
    jurisdiction_analysis: Dict[str, str]
    generated_at: datetime

class AgentResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    processing_time: float

class SubtaskResult(BaseModel):
    task_type: str
    success: bool
    data: Any
    processing_time: float
    retry_count: int = 0 