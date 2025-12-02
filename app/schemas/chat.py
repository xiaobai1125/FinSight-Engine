from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="用户问题")
    use_agent: bool = Field(default=True, description="是否启用计算器 Agent")
    history: List[Dict] = Field(default=[], description="对话历史")

class SourceDocument(BaseModel):
    content: str
    source: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument] = []
    tool_used: Optional[str] = None
    latency_ms: float