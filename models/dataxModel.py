from typing import Optional

from pydantic import BaseModel

from models.excelModel import ExcelModel


class DataxModel(BaseModel):
    reader: str
    writer: str
    writer_conf: str
    ddlType: str
    hikapiConf: Optional[str] = None
    parameter: Optional[str] = None
    excelInfo: Optional[ExcelModel] = None