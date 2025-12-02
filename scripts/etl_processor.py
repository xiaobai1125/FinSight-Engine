import time
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import os


def process_file(filepath):
    max_retries = 3
    for i in range(max_retries):
        try:
            logger.info(f"Processing (Try {i + 1}): {filepath}")
            time.sleep(0.1)  # 模拟耗时
            if "bad" in filepath:
                raise ValueError("File Corrupted")
            logger.success(f"Done: {filepath}")
            return
        except Exception as e:
            logger.warning(f"Error: {e}")
            if i == max_retries - 1:
                logger.error(f"【DLQ】Moved to Dead Letter Queue: {filepath}")


if __name__ == "__main__":
    # 模拟文件列表
    files = ["data/report_2025.pdf", "data/hr_policy.pdf", "data/bad_file_001.pdf"]

    logger.info("Starting ETL Pipeline...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_file, files)