from pydantic import BaseModel

class FileModel(BaseModel):
    filePath: str