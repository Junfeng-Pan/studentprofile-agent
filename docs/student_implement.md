
## 学生能力建模模块 (Student Profiling) 详细实现文档

### 1. 模块、类及调用依赖关系

整个模块采用经典的控制流管道（Pipeline）设计，分为核心调度层、大模型服务层、数据模型层和工具层。

-   **`StudentProfilerPipeline` (核心调度类)**
    -   负责串联业务流，从文件读取到 LLM 结构化提取。
-   **`QwenExtractionService` (大模型抽取服务类)**
    -   利用 LangChain 的 `with_structured_output` 绑定 Pydantic 模型，强制输出固定 Schema。
-   **`DocumentExtractor` (文档提取适配器)**
    -   统一不同格式（PDF/Word）文档的读取接口。

### 2. 接口规范与 JSON Schema 约束实现

在 `schemas.py` 中定义以下规范，确保模型输出与业务逻辑同步：

Python

```python
from pydantic import BaseModel, Field
from typing import List, Literal

class Skill(BaseModel):
    name: str = Field(..., description="技能名称，例如：SpringBoot, MySQL")
    evidence: str = Field(default="", description="简历中支撑该技能的原文，精准截取")

class Certificate(BaseModel):
    name: str = Field(..., description="证书名称，例如：英语六级")
    evidence: str = Field(default="", description="简历中支撑该证书的原文，精准截取")

class ExperienceItem(BaseModel):
    name: str = Field(..., description="项目或者实习经历的名称")
    evidence: str = Field(default="", description="简历中支撑该经历的原文描述")

class ScoreLevel(BaseModel):
    # 评分级别约束为 Literal，确保模型仅输出“高/中/低”
    level: Literal["高", "中", "低"] = Field(default="低", description="评分，可选值：高、中、低")

class StudentProfile(BaseModel):
    """提取的学生简历结构化信息"""
    skills: List[Skill] = Field(default_factory=list, description="提取学生技能集合")
    certificates: List[Certificate] = Field(default_factory=list, description="提取学生相关证书")
    Experience: List[ExperienceItem] = Field(default_factory=list, description="提取项目经历与实习经历信息")
    Professionalism: ScoreLevel = Field(default_factory=lambda: ScoreLevel(level="低"), description="职业素养评分")
    Potential: ScoreLevel = Field(default_factory=lambda: ScoreLevel(level="低"), description="发展潜力评分")
```

**关键变更说明**：
1.  **Skill 模型精简**：去除了 `level` 字段，因为大模型对技能熟练度的量化打分存在较高主观性，改为通过 `evidence` 提供原文依据。
2.  **定性评估**：`Professionalism` 和 `Potential` 的 `level` 字段从整数（1-5）改为文本（"高"、"中"、"低"），更符合大模型对软实力的评估习惯。

### 3. 环境与依赖配置

```bash
pip install fastapi uvicorn python-multipart langchain langchain-openai pydantic pymupdf python-docx pyyaml
```
