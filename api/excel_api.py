from fastapi import APIRouter,Query
from fastapi.responses import PlainTextResponse

from models.excelModel import ExcelConcatModel, ExcelModel2, ExcelModel, ExcelInfo
from models.excel_processor import ExcelProcessor
from models.fileModel import FileModel

router = APIRouter(prefix="/api/excel", tags=["excel"])


@router.post('/parse')
def get_sheet_info(file_info: ExcelInfo):
    e = ExcelProcessor(file_info.filePath)
    data = e.excel_info()
    return data

@router.post('/cols')
def get_sheet_info(excel_info: ExcelInfo):
    e = ExcelProcessor(excel_info.filePath)
    print(e)
    return {
        "columns": e.get_cols(excel_info.sheetName)
    }

@router.post('/sheetInfo')
def get_sheet_info(excelInfo: ExcelModel2):
    e = ExcelProcessor(excelInfo.filePath)
    return e.get_sheet_columns(excelInfo.sheet_name)

@router.post('/convert')
def convert(excel_info: ExcelInfo, output_type: str = Query(...)):
    print(excel_info)
    data = ""
    e = ExcelProcessor(excel_info.filePath)
    if output_type == "json":
        data = e.to_json(excel_info)
    if output_type == "generate_by_template":
        selected_columns = []
        concat_template = ""
        for i in excel_info.colMetadata:
            selected_columns.append(i.col)
            new_i = i.prefix + i.col + i.suffix
            concat_template += new_i

        data = e.concat_columns(sheet_name=excel_info.sheetName,selected_columns=selected_columns,concat_template=concat_template)
    return data

@router.post('/concat-col')
def concat_col(excelInfo: ExcelConcatModel):
    try:
        e = ExcelProcessor(excelInfo.filePath)
        r = e.concat_columns(sheet_name=excelInfo.sheet_name,selected_columns=excelInfo.select_cols,concat_template=excelInfo.concat_template)
        return PlainTextResponse(r)
    except Exception as e:
        return {"error": f"读取 Excel 失败: {str(e)}"}

