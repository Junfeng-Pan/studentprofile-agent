import yaml
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .schemas import StudentProfile

from .prompt import RESUME_EXTRACTION_SYSTEM_PROMPT, RESUME_EXTRACTION_HUMAN_PROMPT

class QwenExtractionService:
    """
    大模型抽取服务类，负责与 Qwen 模型交互并提取结构化简历信息。
    """
    def __init__(self, config_path: str = "config/settings.yaml"):
        # 1. 加载配置
        if not os.path.exists(config_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, config_path)
            
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件未找到: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        llm_config = config.get('llm', {})
        self.api_key = llm_config.get('api_key')
        self.base_url = llm_config.get('base_url')
        self.model_name = llm_config.get('model_name')

        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            if not self.api_key:
                raise ValueError("请在 config/settings.yaml 中填写有效的 api_key 或设置 DASHSCOPE_API_KEY 环境变量")

        # 2. 初始化结构化 LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model_name,
            temperature=0
        ).with_structured_output(StudentProfile)

        # 3. 定义 Prompt 模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", RESUME_EXTRACTION_SYSTEM_PROMPT),
            ("human", RESUME_EXTRACTION_HUMAN_PROMPT)
        ])

    def extract_profile(self, text: str) -> StudentProfile:
        """
        核心方法：调用 LLM 提取结构化信息。
        """
        chain = self.prompt | self.llm
        try:
            result = chain.invoke({"resume_text": text})
            return result
        except Exception as e:
            print(f"LLM Extraction Error: {e}")
            return StudentProfile()

    def extract_profile_stream(self, text: str):
        """
        测试用流式方法：直接观察 Token 生成过程。
        """
        # 使用存储在 self 中的参数重新创建一个流式 LLM
        temp_llm = ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model_name,
            temperature=0,
            streaming=True
        )
        
        chain = self.prompt | temp_llm
        
        import time
        print("\n--- 开始流式输出测试 ---")
        start_time = time.time()
        first_token_time = None
        
        try:
            for chunk in chain.stream({"resume_text": text}):
                if first_token_time is None:
                    first_token_time = time.time()
                    print(f"\n[首字响应时间: {first_token_time - start_time:.2f}s]")
                print(chunk.content, end="", flush=True)
                
            print(f"\n\n[总耗时: {time.time() - start_time:.2f}s]")
        except Exception as e:
            print(f"\nStreaming Error: {e}")
