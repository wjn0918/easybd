import logging
import os
import sys
import json
import uuid

import numpy as np
import pandas as pd
from fastapi import APIRouter,File,UploadFile,HTTPException, Query
from fastapi.responses import JSONResponse

from db import ConfigModel, SessionDep
from easybd.conf import JDBCConf
from easybd.datax import DataXReaderType
from easybd.datax.datax_type import DataXWriterType
from easybd.db.ddl import DDLType
from easybd.excel import Excel
from models.dataxModel import DataxModel
from models.excelModel import ExcelModel
from models.fileModel import FileModel
from pathlib import Path

# 确保上传目录存在
UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
directory = Path(UPLOAD_DIR)

# 检查目录是否存在，不存在则创建
directory.mkdir(parents=True, exist_ok=True)


router = APIRouter(prefix="/api", tags=["openapi"])
@router.get("/")
def cs():
    return {"Hello": "World"}
@router.post("/tools/excel/read_local_file")
def read_local_file(fileModel: FileModel):
    file_path = fileModel.filePath
    if not os.path.isfile(file_path):
        return {'message': '文件不存在'}
    # Get sheet names
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    # Store file path in session (or other state management)
    return {"sheets": sheet_names}

@router.post("/tools/excel/process_sheet")
def process_sheet(excelModel: ExcelModel):
    tables = []
    df = pd.read_excel(excelModel.filePath, sheet_name=excelModel.sheet)
    if len(df) == 0:
        return {"tables": tables}
    try:
        tables = _get_tables(df)
    except Exception as e:
        print(e)
        return {"error": "表拆分失败，查看是否每张表空一行"}
    return {"tables": tables}

@router.post('/tools/db/process_table')
def db_process_table(excelInfo: ExcelModel):

    t = Excel(excelInfo.filePath, sheet_name=excelInfo.sheet, table_name=excelInfo.table)
    t.to_dml2()
    sql_dml = t.to_dml2()
    sql_ddl = t.to_ddl2(DDLType.PgSql)
    j = t.to_field_list()
    fc = t.to_filed_comment()
    return {"sql": sql_ddl, "sqlQuery": sql_dml, "sourceTables": "source_tables", "fieldComment": j, "fc": fc}


@router.post('/tools/db/tojson')
def db_process_sheet2json(excelInfo: ExcelModel):
    try:
        df = pd.read_excel(excelInfo.filePath, sheet_name=excelInfo.sheet)
    except Exception as e:
        return {"error": f"读取 Excel 失败: {str(e)}"}

    try:
        for step in excelInfo.transformSteps:
            if step.action == "filter":
                df = df[eval(step.expr, {"__builtins__": {}}, {"df": df})]
            elif step.action == "assign":
                exec(step.expr, {"__builtins__": {}}, {"df": df})
            elif step.action == "rename":
                df = df.rename(columns=step.expr)
            elif step.action == "dropna":
                df = df.dropna(subset=step.expr)
            else:
                return {"error": f"不支持的操作类型: {step.action}"}
    except Exception as e:
        return {"error": f"处理数据失败: {str(e)}"}

    return df.to_json(orient='records', force_ascii=False)

@router.post("/tools/excel/datax/process_table")
def process_table(dataxModel: DataxModel):
    """
    {
    "readerJdbcUrl": "jdbc:postgresql://10.200.10.22:5432/schooletl",
    "readerUserName": "postgres",
    "readerPassword": "Pgsql@2024",
    "writerJdbcUrl": "jdbc:postgresql://192.168.3.205:5432/schooletl",
    "writerUserName": "postgres",
    "writerPassword": "Pgsql@2024"

}
    :param dataxModel:
    :return:
    """
    excelInfo = dataxModel.excelInfo
    print(dataxModel)
    try:
        datax_conf = json.loads(dataxModel.parameter)
        print(datax_conf)
    except Exception as e:
        print("datax 未配置")



    reader_type: DataXReaderType = DataXReaderType.__members__.get(dataxModel.reader)
    writer_type: DataXWriterType = DataXWriterType.__members__.get(dataxModel.writer)

    ddl_type: DDLType = DDLType.__members__.get(dataxModel.ddlType)

    source_host = "10.200.10.22"
    source_port = 5432
    source_db = "schooletl"
    source_user = "postgres"
    source_password = "Pgsql@2024"
    jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)

    target_host = "47.97.35.199"
    target_port = 54321
    target_db = "tx"
    target_user = "postgres"
    target_password = "Pgsql@2024"
    target_jdbc_conf = JDBCConf("pgsql", target_host, target_port, target_db, target_user, target_password)

    t = Excel(excelInfo.filePath, sheet_name=excelInfo.sheet, table_name=excelInfo.table)
    datax_json = t.to_datax(reader_type, writer_type, t.table_meta[0], jdbc_conf, target_jdbc_conf)
    print(ddl_type)
    ddl_json = t.to_ddl2(ddl_type)

    # 数据库更改
    if reader_type == DataXReaderType.PGSQL or reader_type == DataXReaderType.MYSQL:
        datax_json = json.loads(datax_json)
        datax_json['job']['content'][0]['reader']['parameter']['connection'][0]['jdbcUrl'][0] = datax_conf['readerJdbcUrl']
        datax_json['job']['content'][0]['reader']['parameter']['username'] = datax_conf['readerUserName']
        datax_json['job']['content'][0]['reader']['parameter']['password'] = datax_conf['readerPassword']
        datax_json['job']['content'][0]['writer']['parameter']['connection'][0]['jdbcUrl'] = datax_conf['writerJdbcUrl']
        datax_json['job']['content'][0]['writer']['parameter']['username'] = datax_conf['writerUserName']
        datax_json['job']['content'][0]['writer']['parameter']['password'] = datax_conf['writerPassword']
        datax_json = json.dumps(datax_json)
    if writer_type == DataXWriterType.PGSQL:
        datax_json = json.loads(datax_json)
        writer_conf = json.loads(dataxModel.writer_conf)
        datax_json['job']['content'][0]['writer']['parameter']['connection'][0]['jdbcUrl'] = writer_conf['jdbcUrl']
        datax_json['job']['content'][0]['writer']['parameter']['username'] = writer_conf['userName']
        datax_json['job']['content'][0]['writer']['parameter']['password'] = writer_conf['passwd']
    if reader_type ==DataXReaderType.HIKAPI:
        if isinstance(datax_json, str):
            datax_json = json.loads(datax_json)
        hikapiConf = json.loads(dataxModel.hikapiConf)
        print(f"hikapiConf : {hikapiConf}")
        datax_json['job']['content'][0]['reader']['parameter']['host'] = hikapiConf['host']
        datax_json['job']['content'][0]['reader']['parameter']['appKey'] = hikapiConf['appKey']
        datax_json['job']['content'][0]['reader']['parameter']['appSecret'] = hikapiConf['appSecret']
        datax_json['job']['content'][0]['reader']['parameter']['jsonData'] = hikapiConf['jsonData']
        if writer_type == DataXWriterType.STREAM:
            datax_json['job']['content'][0]['reader']['parameter']['page']["ifPage"] = False
        datax_json = json.dumps(datax_json)
    print(datax_json)

    return {"datax": datax_json, "sql_ddl": ddl_json}

@router.get("/tools/excel/datax/get_datax_type")
def get_datax_type():
    """支持的datax 类型"""
    return {
        "datax_reader_type": [i.name for i in list(DataXReaderType)],
        "datax_writer_type": [i.name for i in list(DataXWriterType)],
        "ddl_type": [i.name for i in list(DDLType)]
    }

def _get_tables(df: pd.DataFrame) -> list:
    """
    获取sheet中所有的表
    :param df:
    :return:
    """
    table_list = df[['表名','表备注']].drop_duplicates().apply(lambda x: tuple(x), axis=1).values.tolist()
    return table_list


@router.post('/tools/excel/upload')
async def upload_file(session: SessionDep, file: UploadFile = File(...)):
    try:
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, filename)

        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        full_file_path = os.path.join(os.getcwd(), file_path)

        # 先查询数据库是否有该文件名记录
        conf = session.query(ConfigModel).filter_by(confName=filename).first()
        if conf:
            # 更新已有记录
            conf.confContent = full_file_path
            session.commit()
            session.refresh(conf)
        else:
            # 新增记录
            conf = ConfigModel(id=str(uuid.uuid4()), confType="excel", confName=filename, confContent=full_file_path)
            session.add(conf)
            session.commit()
            session.refresh(conf)

        return JSONResponse(status_code=200, content="上传成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/tools/excel/check-file-exist")
async def check_file_exist(filename: str = Query(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    exists = os.path.isfile(file_path)
    return JSONResponse(content={"exists": exists})