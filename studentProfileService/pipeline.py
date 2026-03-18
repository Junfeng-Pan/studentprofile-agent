from documentService import DocumentExtractor
from agentService import QwenExtractionService
import os

class StudentProfilerPipeline:
    """
    核心调度类，负责串联文档解析、文本清洗和 LLM 提取的完整业务流。
    """
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.extractor = DocumentExtractor()
        self.extraction_service = QwenExtractionService(config_path=config_path)

    def process_file(self, file_path: str) -> dict:
        """
        接收 PDF/Word 文件路径，执行提取并返回结构化字典。
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"简历文件未找到: {file_path}")
            
        # 1. 调用 DocumentExtractor 进行解析和清洗
        # 注意：DocumentExtractor.extract 内部已经调用了 clean_whitespace 和 remove_garbled_chars
        cleaned_text = self.extractor.extract(file_path)
        
        # 2. 调用 QwenExtractionService 进行 LLM 提取
        profile = self.extraction_service.extract_profile(cleaned_text)
        
        # 3. 返回 Pydantic 模型的字典形式
        return profile.model_dump()

    def process_text(self, raw_text: str) -> dict:
        """
        直接处理用户录入的非结构化文本。
        """
        if not raw_text or not raw_text.strip():
            return {}
            
        # 调用 LLM 提取
        profile = self.extraction_service.extract_profile(raw_text)
        return profile.model_dump()
