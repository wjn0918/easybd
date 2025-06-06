from typing import Optional, Union, Dict, List

from pydantic import BaseModel


class TransformStep(BaseModel):
    action: str  # filter, assign, rename, dropna 等
    expr: Union[str, Dict, List[str]]

class ExcelModel(BaseModel):
    filePath: str
    sheet: str
    table: Optional[str] = ""
    transformSteps: List[TransformStep] = []