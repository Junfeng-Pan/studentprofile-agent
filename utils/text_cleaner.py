import re

def clean_whitespace(text: str) -> str:
    """
    去除多余的水平空格和不可见字符，但保留换行符以维持文本结构。
    1. 将连续的水平空白（空格、制表符）替换为单个空格。
    2. 去除每行开头和结尾的空格。
    3. 将三个及以上的连续换行符替换为两个（保留段落间隙）。
    """
    # 1. 替换水平空白（空格、制表符）为单个空格
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 2. 去除每行首尾的空格
    lines = [line.strip() for line in text.split('\n')]
    
    # 3. 重新组合并处理过度换行
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def remove_garbled_chars(text: str) -> str:
    """
    通过正则表达式剔除常见的乱码字符或非打印字符。
    """
    # 过滤掉非打印字符（除了常用的控制字符如换行和制表符）
    text = "".join(ch for ch in text if ch.isprintable() or ch in ['\n', '\r', '\t'])
    return text
