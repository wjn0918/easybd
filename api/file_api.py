import os
import uuid

from fastapi import APIRouter, UploadFile,File,HTTPException
from fastapi.responses import JSONResponse

from db import SessionDep, ConfigModel
from pathlib import Path

router = APIRouter(prefix="/api/file", tags=["file"])

# 确保上传目录存在
UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
directory = Path(UPLOAD_DIR)

# 检查目录是否存在，不存在则创建
directory.mkdir(parents=True, exist_ok=True)

@router.post('/upload')
async def upload_file(session: SessionDep, file: UploadFile = File(...)):
    try:
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, filename)

        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        full_file_path = os.path.join(os.getcwd(), file_path)

        # 先查询数据库是否有该文件名记录
        conf = session.query(ConfigModel).filter_by(confName=filename).first()
        if conf:
            # 更新已有记录
            conf.confContent = full_file_path
            session.commit()
            session.refresh(conf)
        else:
            # 新增记录
            conf = ConfigModel(id=str(uuid.uuid4()), confType="excel", confName=filename, confContent=full_file_path)
            session.add(conf)
            session.commit()
            session.refresh(conf)

        return JSONResponse(status_code=200, content={"file_path": full_file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")