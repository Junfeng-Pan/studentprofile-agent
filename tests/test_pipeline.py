import os
import sys
import pytest
import time
import json

# 1. 环境准备
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from studentProfileService import StudentProfilerPipeline

# 更新测试资源路径
RESOURCES_DIR = os.path.join(BASE_DIR, "tests", "resourcesForTests")
WORD_PATH = os.path.join(RESOURCES_DIR, "测试简历01.docx")
PDF_PATH = os.path.join(RESOURCES_DIR, "测试简历02.pdf")

@pytest.fixture
def pipeline():
    return StudentProfilerPipeline()

def test_pipeline_process_word(pipeline):
    """
    测试 Word 简历并输出结果与响应时间。
    """
    if not os.path.exists(WORD_PATH):
        pytest.skip(f"Word 测试文件不存在: {WORD_PATH}")
    
    print(f"\n[开始处理 Word 简历]: {os.path.basename(WORD_PATH)}")
    start_time = time.time()
    
    result = pipeline.process_file(WORD_PATH)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n[响应时间]: {duration:.2f}s")
    print("[模型输出结果]:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    assert isinstance(result, dict)
    assert "skills" in result

def test_pipeline_process_pdf(pipeline):
    """
    测试 PDF 简历并输出结果与响应时间。
    """
    if not os.path.exists(PDF_PATH):
        pytest.skip(f"PDF 测试文件不存在: {PDF_PATH}")
    
    print(f"\n[开始处理 PDF 简历]: {os.path.basename(PDF_PATH)}")
    start_time = time.time()
    
    result = pipeline.process_file(PDF_PATH)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n[响应时间]: {duration:.2f}s")
    print("[模型输出结果]:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    assert isinstance(result, dict)
    assert "skills" in result

def test_pipeline_process_raw_text(pipeline):
    """
    测试纯文本处理并输出结果与响应时间。
    """
    test_text = "姓名：李华，熟悉 Python 和 Django，曾主导过一个电商后台项目。"
    print("\n[开始处理纯文本输入]")
    start_time = time.time()
    
    result = pipeline.process_text(test_text)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n[响应时间]: {duration:.2f}s")
    print("[模型输出结果]:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    assert isinstance(result, dict)
