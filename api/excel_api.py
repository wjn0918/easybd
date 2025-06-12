import io
import json

import pandas as pd
from fastapi import APIRouter,Query
from fastapi.responses import PlainTextResponse,StreamingResponse

from models.excelModel import ExcelConcatModel, ExcelModel2, ExcelModel, ExcelInfo, JsonModel
from models.excel_processor import ExcelProcessor
from models.fileModel import FileModel

router = APIRouter(prefix="/api/excel", tags=["excel"])


@router.post('/parse')
def get_sheet_info(file_info: FileModel):
    e = ExcelProcessor(file_info.filePath)
    data = e.get_sheets()
    return data

@router.post('/cols')
def get_sheet_info(excel_info: ExcelInfo):
    e = ExcelProcessor(excel_info.filePath)
    print(e)
    return {
        "columns": e.get_cols(excel_info.sheetName)
    }

@router.post('/tables')
def get_sheet_tables(excel_info: ExcelInfo):
    e = ExcelProcessor(excel_info.filePath)
    print(e.get_tables(excel_info.sheetName))
    return {
        "tables": e.get_tables(excel_info.sheetName)
    }

@router.post('/sheetInfo')
def get_sheet_info(excelInfo: ExcelModel2):
    e = ExcelProcessor(excelInfo.filePath)
    return e.get_sheet_columns(excelInfo.sheet_name)

@router.post('/convert')
def convert(excel_info: ExcelInfo, output_type: str = Query(...)):
    data = ""
    e = ExcelProcessor(excel_info.filePath, excel_info)
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
    if output_type == "datax":
        print(excel_info)
        data = e.to_datax()
    return data

@router.post('/convert2excel')
def convert2excel(jsonModel: JsonModel):
    try:

        data = json.loads(jsonModel.jsonData)
    except Exception as e:
        return {"error": f"json 加载失败: {str(e)}"}
    try:
        # 自动从 JSON 生成 DataFrame（字段自动识别）
        df = pd.DataFrame(data)

        # 写入 Excel 到内存
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)  # 不指定列，输出所有字段

        output.seek(0)

        # 构造下载响应
        headers = {
            "Content-Disposition": 'attachment; filename="export.xlsx"'
        }
        return StreamingResponse(output,
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers=headers)
    except Exception as e:
        return {"error": f"生成 Excel 失败: {str(e)}"}

@router.post('/concat-col')
def concat_col(excelInfo: ExcelConcatModel):
    try:
        e = ExcelProcessor(excelInfo.filePath)
        r = e.concat_columns(sheet_name=excelInfo.sheet_name,selected_columns=excelInfo.select_cols,concat_template=excelInfo.concat_template)
        return PlainTextResponse(r)
    except Exception as e:
        return {"error": f"读取 Excel 失败: {str(e)}"}

