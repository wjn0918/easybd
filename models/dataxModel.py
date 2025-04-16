from typing import Optional

from pydantic import BaseModel

from models.excelModel import ExcelModel


class DataxModel(BaseModel):
    reader: str
    writer: str
    ddlType: str
    hikapiConf: str
    parameter: Optional[str] = None
    excelInfo: Optional[ExcelModel] = None