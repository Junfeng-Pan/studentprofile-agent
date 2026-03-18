import os
from utils import read_pdf, read_word, clean_whitespace, remove_garbled_chars

class DocumentExtractor:
    """
    文档提取适配器，统一不同格式文档的读取接口。
    """
    def extract(self, file_path: str) -> str:
        """
        根据文件后缀自动选择解析工具，并对提取出的文本进行基础清洗。
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        raw_text = ""

        # 1. 根据后缀路由到不同的解析方法
        if ext == '.pdf':
            raw_text = read_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            raw_text = read_word(file_path)
        else:
            raise ValueError(f"暂不支持的文件格式: {ext}")

        # 2. 调用清洗工具进行基础处理
        # 先剔除乱码/非打印字符，再清理多余空白
        cleaned_text = remove_garbled_chars(raw_text)
        cleaned_text = clean_whitespace(cleaned_text)

        return cleaned_text
