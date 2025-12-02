import sys
from loguru import logger


def setup_logging():
    """配置日志：控制台高亮 + 文件轮转"""
    logger.remove()

    # 控制台
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # 文件 (按天轮转)
    logger.add(
        "logs/finsight.log",
        rotation="00:00",
        retention="7 days",
        level="INFO",
        enqueue=True
    )


setup_logging()