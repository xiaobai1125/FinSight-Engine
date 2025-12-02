import re
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

# 引入 LangChain 的切片器
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 模拟待处理的文件
files_to_process = [f"report_{i}.pdf" for i in range(1, 21)]
dlq_list = []


# Chunk Size 设为 1000，Overlap 设为 200，防止语义断层
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", "。", "！", "？"]
)


def process_single_file(filename):
    """模拟单个文件的 ETL 流程：读取 -> 清洗 -> 切片 -> 入库"""
    try:
        logger.info(f"开始处理: {filename}")
        # === 真实生产环境代码 (已注释) ===
        # from langchain_community.document_loaders import PyPDFLoader
        # loader = PyPDFLoader(f"./data/{filename}")
        # docs = loader.load()
        # raw_text = " ".join([d.page_content for d in docs])
        # ==============================

        # === 演示环境代码 (Mock) ===
        # 1. 模拟读取 PDF 内容
        # 在真实场景用 PyPDFLoader(filename).load()
        raw_text = f"这里是 {filename} 的模拟内容..." * 500

        # 2. 模拟正则清洗 (Regex),这里是核心通用的几条
        cleaning_rules = [
            (r'\d+/\d+', ''),  # 去除页码 (如 1/20)
            (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL]'),  # 邮箱脱敏
            (r'Confidential|机密文件', ''),  # 去除水印关键词
            (r'^\s*$', ''),  # 去除空行
            (r'\u3000', ' '),  # 替换全角空格
            # ... (More rules loaded from config in production)
        ]

        clean_text = raw_text
        for pattern, replacement in cleaning_rules:
            clean_text = re.sub(pattern, replacement, clean_text)

        # 3. 执行切片 (Chunking)
        chunks = text_splitter.split_text(clean_text)
        logger.info(f"文件 {filename} 被切分为 {len(chunks)} 个片段")

        # 4. 模拟入库 (Embedding)
        time.sleep(random.uniform(0.1, 0.5))  # 模拟向量化耗时

        return True

    except Exception as e:
        logger.error(f"处理失败: {filename} - {str(e)}")
        dlq_list.append({"file": filename, "error": str(e)})
        return False


def main():
    logger.info("启动多线程 ETL 流水线...")

    # 多线程并发处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_single_file, files_to_process)

    if dlq_list:
        with open("failed_jobs.json", "w") as f:
            json.dump(dlq_list, f)
        logger.warning(f"异常任务已写入死信队列，共 {len(dlq_list)} 个")


if __name__ == "__main__":
    main()
