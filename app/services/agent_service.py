import re
from langchain_core.tools import tool
from app.core.logger import logger


class AgentLiteService:
    """
    轻量级 Agent，用于处理数值计算意图
    """

    @staticmethod
    def _is_math_intent(query: str) -> bool:
        # 简单关键词匹配：包含数字 且 包含计算词
        keywords = ["+", "-", "*", "/", "乘以", "除以", "加", "减", "增长率"]
        has_digit = any(c.isdigit() for c in query)
        has_kw = any(k in query for k in keywords)
        return has_digit and has_kw

    @tool
    def calculator(expression: str) -> str:
        """执行数学运算"""
        try:
            # 安全清洗，只保留数字和运算符
            safe_expr = re.sub(r"[^0-9+\-*/(). ]", "", expression)
            return str(eval(safe_expr))
        except:
            return "Error"

    async def run(self, query: str) -> str | None:
        if self._is_math_intent(query):
            logger.info(f"[Agent] 识别到计算意图: {query}")
            # 模拟 LLM 提取公式的过程 (这里用正则简化演示)
            # 例如输入 "100 * 50"，提取 "100 * 50"
            try:
                match = re.search(r"[\d\.\s\+\-\*\/]+", query)
                if match:
                    expr = match.group(0).strip()
                    if len(expr) > 2:  # 避免提取单个数字
                        res = eval(expr)
                        return f"经 Agent 计算，结果为: **{res}**"
            except Exception as e:
                logger.warning(f"[Agent] 计算提取失败: {e}")
        return None