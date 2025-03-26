from pydantic import BaseModel
class ConfigModel(BaseModel):
    confType:str
    confName:str
    confContent:str