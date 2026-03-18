import sys
import os
import json
import argparse
from studentProfileService import StudentProfilerPipeline

def main():
    parser = argparse.ArgumentParser(description="学生能力建模模块 - 简历解析工具")
    parser.add_argument("file", help="要解析的简历文件路径 (PDF 或 Word)")
    parser.add_argument("--config", default="config/settings.yaml", help="配置文件路径")
    
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误: 找不到文件 '{args.file}'")
        sys.exit(1)

    print(f"[*] 正在初始化引擎...")
    try:
        pipeline = StudentProfilerPipeline(config_path=args.config)
    except Exception as e:
        print(f"[-] 初始化失败: {e}")
        sys.exit(1)

    print(f"[*] 正在解析简历: {os.path.basename(args.file)} ...")
    try:
        # 这里使用了 pipeline 封装好的端到端流程
        result = pipeline.process_file(args.file)
        print("\n[+] 结构化能力提取成功:")
        print("=" * 50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 50)
    except Exception as e:
        print(f"[-] 处理过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
