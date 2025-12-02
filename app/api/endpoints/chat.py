import time
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, SourceDocument
from app.services.agent_service import AgentLiteService
from app.services.rag_service import RAGService
from app.core.logger import logger

router = APIRouter()


def get_agent(): return AgentLiteService()


def get_rag(): return RAGService()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
        request: ChatRequest,
        agent: AgentLiteService = Depends(get_agent),
        rag: RAGService = Depends(get_rag)
):
    start_time = time.time()
    answer = ""
    tool_used = None

    try:
        # 1. 优先尝试 Agent 计算
        if request.use_agent:
            res = await agent.run(request.query)
            if res:
                answer = res
                tool_used = "Calculator"

        # 2. 如果不是计算，走 RAG
        if not answer:
            answer = await rag.search(request.query)

        # 模拟返回来源
        sources = [SourceDocument(content="员工手册.pdf", source="HR Policy")]

        latency = (time.time() - start_time) * 1000

        return ChatResponse(
            answer=answer,
            sources=sources,
            tool_used=tool_used,
            latency_ms=round(latency, 2)
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Server Error")