import os
import pytest
import sys

# 测试资源文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到Python的模块搜索路径中（关键修复）
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from documentService import DocumentExtractor




RESOURCES_DIR = os.path.join(BASE_DIR, "tests", "resourcesForTests")

PDF_PATH = os.path.join(RESOURCES_DIR, "masquant.pdf")
WORD_PATH = os.path.join(RESOURCES_DIR, "美赛.docx")

@pytest.fixture
def extractor():
    return DocumentExtractor()

def test_extract_pdf(extractor):
    """
    测试 PDF 提取功能。
    """
    if not os.path.exists(PDF_PATH):
        pytest.skip(f"PDF 测试文件不存在: {PDF_PATH}")
    
    text = extractor.extract(PDF_PATH)
    assert isinstance(text, str)
    assert len(text) > 0
    # 打印前 100 个字符进行观察
    print(f"\nPDF 提取内容预览: {text[:100]}...")

def test_extract_word(extractor):
    """
    测试 Word 提取功能。
    """
    if not os.path.exists(WORD_PATH):
        pytest.skip(f"Word 测试文件不存在: {WORD_PATH}")
    
    text = extractor.extract(WORD_PATH)
    assert isinstance(text, str)
    assert len(text) > 0
    # 打印前 100 个字符进行观察
    print(f"\nWord 提取内容预览: {text[:100]}...")

def test_invalid_file_format(extractor):
    """
    测试不支持的文件格式应抛出异常。
    """
    invalid_file = "test.txt"
    # 创建临时 txt 文件
    with open(invalid_file, "w") as f:
        f.write("test content")
    
    with pytest.raises(ValueError, match="暂不支持的文件格式"):
        extractor.extract(invalid_file)
    
    os.remove(invalid_file)

def test_file_not_found(extractor):
    """
    测试文件不存在时应抛出异常。
    """
    with pytest.raises(FileNotFoundError):
        extractor.extract("non_existent_file.pdf")
