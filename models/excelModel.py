from typing import Optional

from pydantic import BaseModel


class ExcelModel(BaseModel):
    filePath: str
    sheet: str
    table: Optional[str] = ""
    filterExpr: Optional[str] = None  # 新增字段