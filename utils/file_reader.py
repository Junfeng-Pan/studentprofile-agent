import fitz  # PyMuPDF
from docx import Document

def read_pdf(file_path: str) -> str:
    """
    使用 PyMuPDF 读取 PDF 并提取所有页面的文本。
    """
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def read_word(file_path: str) -> str:
    """
    使用 python-docx 读取 Word 文档的段落。
    """
    text = ""
    try:
        doc = Document(file_path)
        # 获取所有段落文本并用换行符连接
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Error reading Word {file_path}: {e}")
    return text
