# 📈 FinSight Engine - 企业智能知识库引擎 

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**FinSight Engine** 是一套面向企业内部垂直领域的智能问答解决方案。它基于 **RAG (检索增强生成)** 与 **Agent Lite (轻量级智能体)** 架构，解决了传统大模型在私有知识检索准确率低、数值计算易幻觉等痛点。

本项目采用生产级工程规范构建，包含从 **多源异构数据清洗 (ETL)** 到 **高并发异步接口 (Async API)** 的全链路实现。

------

## ✨ 核心特性 (Key Features)

### 1. 🤖 Agentic RAG 混合架构

- **智能路由 (Router)：** 自动识别用户意图。若涉及知识问答，调用 RAG 检索链路；若涉及复杂数值计算（如财报增长率），自动调度 **Calculator Tool**。
- **DeepSeek 驱动：** 底层接入 DeepSeek-V3 模型，提供高性价比的推理能力。

### 2. 🕷️ 高鲁棒性 ETL 流水线

- **多线程并发：** 基于 `ThreadPoolExecutor` 实现百万级文档的高效清洗。
- **死信队列 (DLQ)：** 内置异常重试机制，自动将损坏文件移入死信队列，保障主流程不崩溃。
- **正则清洗：** 内置 30+ 组金融/法务文档专用正则规则，精准去除页眉、水印与乱码。

### 3. ⚡ 生产级工程规范

- **FastAPI 异步架构：** 全面采用 `Async/Await` 与 `Dependency Injection`（依赖注入）设计模式。
- **Pydantic V2 校验：** 严格的 Request/Response Schema 定义，杜绝字段缺失引发的 `KeyError`。
- 可观测性 (Observability)：
  - 集成 **Loguru** 实现日志自动轮转与结构化输出。
  - 预置 **Sentry** 监控埋点，实时追踪线上异常堆栈。

------

## 📂 目录结构

text

```
FinSight-Engine/
├── app/
│   ├── api/              # API 路由与依赖注入层
│   ├── core/             # 核心配置 (Config / Logger)
│   ├── schemas/          # Pydantic 数据模型定义
│   ├── services/         # 业务逻辑层 (Agent / RAG Service)
│   └── main.py           # 应用启动入口
├── logs/ 
│   ├── api/              # 记录日志
├── scripts/
│   └── etl_processor.py  # 多线程 ETL 清洗脚本 (含 DLQ 演示)
├── data/                 # 演示用测试文档 (PDF)
├── demo_ui.py            # Streamlit 演示前端
├──	Dockerfile			  # 镜像构建
├── docker-compose.yml    # 容器编排配置
└── requirements.txt      # 依赖清单
```

------

## 🚀 快速开始 (Quick Start)

### 1. 环境准备

Bash

```
# 克隆仓库
git clone https://github.com/xiaobai1125/FinSight-Engine.git
cd FinSight-Engine

# 创建并激活虚拟环境 (可选)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

打开 `app/core/config.py`，填入您的 DeepSeek 或 OpenAI Key：

Python

```
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx"
OPENAI_BASE_URL = "https://api.deepseek.com"
```

### 3. 启动服务

**启动后端 (FastAPI):**

Bash

```
# 使用模块方式启动，避免路径报错
python -m app.main
```

*后端将在 http://127.0.0.1:8000 启动，访问 /docs 可查看 Swagger 文档。*

**启动前端 (Streamlit):**

Bash

```
# 新开一个终端窗口
streamlit run demo_ui.py
```

------

## 🖥️ 演示场景 (Demo Scenarios)

### 场景一：企业制度问答 (RAG)

> **用户提问：** "迟到扣多少钱？"
> **系统回答：** "根据考勤制度，每月允许迟到3次，超过后每次扣款100元。"
> *(底层逻辑：检索 Mock 知识库 -> 注入 Prompt -> DeepSeek 生成)*

### 场景二：数值计算 (Agent)

> **用户提问：** "计算 5000 * 1.2 + 300"
> **系统回答：** "经计算，结果为: 6300.0"
> *(底层逻辑：意图识别 -> 提取公式 -> 调用 Calculator Tool)*

### 场景三：ETL 容错演示

运行清洗脚本，观察 **死信队列** 触发机制：

Bash

```
python scripts/etl_processor.py
```

*控制台将输出红色 Error 日志，表明坏文件已被自动隔离。*

------

## 🛠️ 技术栈

- **Language:** Python 3.10
- **Web Framework:** FastAPI, Uvicorn
- **LLM Framework:** LangChain
- **Data Processing:** Pandas, Regex
- **Observability:** Loguru, Sentry

- **Deployment:** Docker, Docker-Compose

