from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.core.logger import logger


class RAGService:
    def __init__(self):
        # 初始化 DeepSeek
        try:
            self.llm = ChatOpenAI(
                model_name=settings.MODEL_NAME,
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_BASE_URL,
                temperature=0.1
            )
            logger.info("DeepSeek 模型已连接")
        except Exception:
            logger.error("模型配置错误，请检查 API Key")

    async def search(self, query: str) -> str:
        logger.info(f"[RAG] 开始处理: {query}")

        # 1. Mock 检索到的文档 (假装是从 ChromaDB 查出来的)
        # 这些内容 DeepSeek 会读到，并根据这些回答
        retrieved_context = (
            "【员工手册-考勤篇】\n"
            "1. 工作时间：09:00 - 18:00，双休。\n"
            "2. 迟到规则：每月有 3 次 10分钟内的豁免权。超过3次或超过30分钟，每次扣款 100 元。\n"
            "【财务报销规范】\n"
            "1. 住宿标准：一线城市 600元/天，二线城市 400元/天。\n"
            "2. 交通费：必须提供纸质发票，打车需备注行程。"
        )

        # 2. 组装 Prompt
        prompt = ChatPromptTemplate.from_template(
            # 修改前：
# 如果资料里没有提到，请说“知识库中未找到相关信息”。

# 修改后（增加闲聊兜底）：
"""
你是一个企业智能助手 (FinSight AI)。
对于【你是谁】、【你好】等闲聊问题，请礼貌地自我介绍。
对于业务问题，请严格基于下方的【参考资料】回答。
如果资料里没有，请说“知识库中未找到相关信息”。

【参考资料】：
{context}

【问题】：
{question}
"""
        )

        # 3. 调用 DeepSeek
        try:
            chain = prompt | self.llm | StrOutputParser()
            response = await chain.ainvoke({
                "context": retrieved_context,
                "question": query
            })
            return response
        except Exception as e:
            logger.error(f"DeepSeek 调用失败: {e}")
            return "抱歉，AI 服务暂时不可用。"