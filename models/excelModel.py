from typing import Optional, Union, Dict, List

from pydantic import BaseModel

from models.fileModel import FileModel


class JsonModel(BaseModel):
    jsonData: str

class TransformStep(BaseModel):
    action: str  # filter, assign, rename, dropna 等
    expr: Union[str, Dict, List[str]]

class ExcelModel(BaseModel):
    filePath: str
    sheet: str
    table: Optional[str] = ""
    transformSteps: List[TransformStep] = []

class ExcelModel2(FileModel):
    sheet_name: str

class ColMetadata(BaseModel):
    col: str
    prefix: str
    suffix: str

class DataXConf(BaseModel):
    readerType: str
    writerType: str
    parameter: Optional[str] = ""

class SqlConf(BaseModel):
    sqlType: str
    dbType: str

class ExcelInfo(FileModel):
    sheetName: Optional[str] = ""
    tableName: Optional[str] = ""
    dataXConf: Optional[DataXConf] = []
    sqlConf: Optional[SqlConf] = []
    transformSteps: List[TransformStep] = []
    colMetadata:List[ColMetadata] = []

class ExcelConcatModel(ExcelModel2):
    select_cols: List[str]
    concat_template: str