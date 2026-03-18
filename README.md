# Student Profile Agent (学生能力建模模块)

该模块旨在利用大语言模型 (LLM) 技术，将非结构化的简历（PDF/Word）或纯文本自动转化为系统可计算的结构化能力向量。

## 核心功能

- **多格式支持**：自动识别并提取 PDF (.pdf) 和 Word (.docx) 文档内容。
- **智能清洗**：自动去除文档乱码、冗余空格，保留分段语义。
- **结构化提取**：基于 LangChain 和 Pydantic 约束，强制 LLM 输出固定 Schema 的 JSON。
- **多维度评分**：自动提取技能、证书、经历，并对职业素养和发展潜力进行 1-5 分量化评估。

## 项目结构

- `agentService/`: LLM 核心服务，包含 Prompt 策略和 Pydantic 模型。
- `documentService/`: 文档解析适配层。
- `studentProfileService/`: 核心业务调度层 (Pipeline)。
- `utils/`: 基础工具包（文件读取、文本清洗）。
- `config/`: 配置文件目录。
- `tests/`: 自动化测试用例。

## 快速开始

### 1. 环境准备
确保已安装 Python 3.9+，并安装依赖：
```bash
pip install langchain langchain-openai pydantic pymupdf python-docx pyyaml pytest
```

### 2. 配置 LLM
在 `config/settings.yaml` 中配置您的 API Key（推荐使用通义千问 Qwen 系列）：
```yaml
llm:
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  api_key: "YOUR_API_KEY"
  model_name: "qwen-plus"
```

### 3. 运行解析
使用 `main.py` 处理单份简历：
```bash
python main.py path/to/your/resume.pdf
```

### 4. 运行测试
执行自动化测试以确保各模块正常运行：
```bash
# 运行完整 Pipeline 测试
pytest -s tests/test_pipeline.py
```

## 技术细节
本项目采用了 LangChain 的 `with_structured_output` 模式，确保了在复杂的简历语境下模型输出的稳定性。所有提取字段均包含 `evidence`（原文证据），以便人工溯源和核验。
