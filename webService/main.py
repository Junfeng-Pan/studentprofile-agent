import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# 环境准备：确保能导入项目模块
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from studentProfileService import StudentProfilerPipeline

# 初始化 FastAPI
app = FastAPI(title="Student Profile API", description="学生简历能力建模解析接口")

# 存储路径配置
UPLOAD_DIR = os.path.join(BASE_DIR, "resources", "files_uploaded")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 初始化业务组件 (全局单例)
try:
    pipeline = StudentProfilerPipeline()
except Exception as e:
    print(f"Error initializing pipeline: {e}")
    pipeline = None

@app.get("/")
async def root():
    return {"message": "Student Profile API is running", "status": "active"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    """
    上传简历文件 (PDF/Word) 并获取解析后的结构化数据
    """
    if not pipeline:
        raise HTTPException(status_code=500, detail="解析引擎初始化失败")

    # 1. 验证文件扩展名
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="仅支持 .pdf 或 .docx 格式文件")

    # 2. 保存文件到本地存储
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    # 3. 调用 Pipeline 处理
    try:
        result = pipeline.process_file(file_path)
        return {
            "success": True,
            "filename": file.filename,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析过程中发生错误: {str(e)}")
    finally:
        # 可选：如果不需要保留文件，可以在此处删除
        # os.remove(file_path)
        pass

if __name__ == "__main__":
    import uvicorn
    # 允许直接运行此文件进行测试
    uvicorn.run(app, host="0.0.0.0", port=8000)
