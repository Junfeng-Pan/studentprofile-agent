import os
import pytest
import sys

# 测试资源文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到Python的模块搜索路径中
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from documentService import DocumentExtractor

# ========== 新增：定义output文件夹路径并确保文件夹存在 ==========
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
# 创建output文件夹（不存在则创建，存在则不报错）
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 测试资源文件路径
RESOURCES_DIR = os.path.join(BASE_DIR, "tests", "resourcesForTests")
PDF_PATH = os.path.join(RESOURCES_DIR, "masquant.pdf")
WORD_PATH = os.path.join(RESOURCES_DIR, "美赛.docx")


@pytest.fixture
def extractor():
    return DocumentExtractor()


def test_extract_pdf(extractor):
    """
    测试 PDF 提取功能：打印全部文本 + 输出到output文件夹。
    """
    if not os.path.exists(PDF_PATH):
        pytest.skip(f"PDF 测试文件不存在: {PDF_PATH}")

    # 提取文本
    text = extractor.extract(PDF_PATH)

    # 原有断言逻辑（保留）
    assert isinstance(text, str)
    assert len(text) > 0

    # ========== 新增：打印全部提取文本 ==========
    print(f"\n=== PDF 提取完整内容 ===")
    print(text)

    # ========== 新增：将文本写入output文件夹 ==========
    pdf_output_path = os.path.join(OUTPUT_DIR, "masquant_extracted.txt")
    with open(pdf_output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\nPDF 提取内容已保存至: {pdf_output_path}")


def test_extract_word(extractor):
    """
    测试 Word 提取功能：打印全部文本 + 输出到output文件夹。
    """
    if not os.path.exists(WORD_PATH):
        pytest.skip(f"Word 测试文件不存在: {WORD_PATH}")

    # 提取文本
    text = extractor.extract(WORD_PATH)

    # 原有断言逻辑（保留）
    assert isinstance(text, str)
    assert len(text) > 0

    # ========== 新增：打印全部提取文本 ==========
    print(f"\n=== Word 提取完整内容 ===")
    print(text)

    # ========== 新增：将文本写入output文件夹 ==========
    word_output_path = os.path.join(OUTPUT_DIR, "美赛_extracted.txt")
    with open(word_output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\nWord 提取内容已保存至: {word_output_path}")


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