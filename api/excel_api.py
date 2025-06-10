from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from models.excelModel import ExcelConcatModel, ExcelModel2
from models.excel_processor import ExcelProcessor

router = APIRouter(prefix="/api/excel", tags=["excel"])

@router.post('/sheetInfo')
def get_sheet_info(excelInfo: ExcelModel2):
    e = ExcelProcessor(excelInfo.filePath)
    return e.get_sheet_columns(excelInfo.sheet_name)



@router.post('/concat-col')
def concat_col(excelInfo: ExcelConcatModel):
    try:
        e = ExcelProcessor(excelInfo.filePath)
        r = e.concat_columns(sheet_name=excelInfo.sheet_name,selected_columns=excelInfo.select_cols,concat_template=excelInfo.concat_template)
        return PlainTextResponse(r)
    except Exception as e:
        return {"error": f"读取 Excel 失败: {str(e)}"}

