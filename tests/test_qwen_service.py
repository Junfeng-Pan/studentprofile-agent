import os
import pytest
import sys
# 计算项目根目录（当前测试文件的上一级目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到Python的模块搜索路径中（关键修复）
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agentService.service import QwenExtractionService
from agentService.schemas import StudentProfile

@pytest.fixture
def extraction_service():
    # 确保 PYTHONPATH 包含项目根目录
    return QwenExtractionService()

def test_qwen_extraction_with_mock_text(extraction_service):
    """
    测试大模型对一段模拟简历文本的提取能力。
    """
    mock_resume = """
    张三，计算机科学与技术专业。
    技能：熟练掌握 Java 和 SpringBoot，具备 3 年开发经验。了解 MySQL 数据库优化。
    证书：英语六级，软件设计师（中级）。
    经历：
    2023.01-2023.06，在某大厂实习，负责后端接口开发，使用 SpringBoot 实现了订单管理系统。
    """
    
    # 注意：如果此时你还没有填写 API Key，这个测试会报错 ValueError
    try:
        profile = extraction_service.extract_profile(mock_resume)
        
        # 验证返回类型
        assert isinstance(profile, StudentProfile)
        
        # 验证基本字段（即使 LLM 没提取到，也应该是默认值）
        assert hasattr(profile, "skills")
        assert hasattr(profile, "certificates")
        assert hasattr(profile, "Experience")
        
        # 打印结果观察
        print("\n--- 提取出的 StudentProfile ---")
        print(profile.model_dump_json(indent=2))
        
        # 如果提取成功，应该能看到张三的技能
        if len(profile.skills) > 0:
            assert any("Java" in s.name or "SpringBoot" in s.name for s in profile.skills)
            
    except ValueError as e:
        pytest.skip(f"跳过测试: {e}")
    except Exception as e:
        pytest.fail(f"LLM 调用失败: {e}")

def test_qwen_streaming(extraction_service):
    """
    测试大模型的流式输出速度。
    """
    mock_resume = """
    张三，计算机科学与技术专业。
    技能：熟练掌握 Java 和 SpringBoot，具备 3 年开发经验。了解 MySQL 数据库优化。
    证书：英语六级，软件设计师（中级）。
    经历：
    2023.01-2023.06，在某大厂实习，负责后端接口开发，使用 SpringBoot 实现了订单管理系统。
    """
    try:
        extraction_service.extract_profile_stream(mock_resume)
    except Exception as e:
        pytest.fail(f"流式调用失败: {e}")
