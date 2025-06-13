from pydantic import BaseModel


class ConfigCreate(BaseModel):
    id:str
    confType: str
    confName: str
    confContent: str