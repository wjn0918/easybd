import logging
import os
import sys
import json

import numpy as np
import pandas as pd
from fastapi import APIRouter

from easybd.conf import JDBCConf
from easybd.datax import DataXReaderType
from easybd.datax.datax_type import DataXWriterType
from easybd.db.ddl import DDLType
from easybd.excel import Excel
from models.dataxModel import DataxModel
from models.excelModel import ExcelModel
from models.fileModel import FileModel

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
    return {"sql": sql_ddl, "sqlQuery": sql_dml, "sourceTables": "source_tables"}


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
    datax_conf = json.loads(dataxModel.parameter)
    print(datax_conf)


    reader_type: DataXReaderType = DataXReaderType.__members__.get(dataxModel.reader)
    writer_type: DataXWriterType = DataXWriterType.__members__.get(dataxModel.writer)

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
    ddl_json = t.to_ddl2(DDLType.PgSql)

    # 数据库更改
    if reader_type == DataXReaderType.PGSQL:
        datax_json = json.loads(datax_json)
        datax_json['job']['content'][0]['reader']['parameter']['connection'][0]['jdbcUrl'][0] = datax_conf['readerJdbcUrl']
        datax_json['job']['content'][0]['reader']['parameter']['username'] = datax_conf['readerUserName']
        datax_json['job']['content'][0]['reader']['parameter']['password'] = datax_conf['readerPassword']
        datax_json['job']['content'][0]['writer']['parameter']['connection'][0]['jdbcUrl'] = datax_conf['writerJdbcUrl']
        datax_json['job']['content'][0]['writer']['parameter']['username'] = datax_conf['writerUserName']
        datax_json['job']['content'][0]['writer']['parameter']['password'] = datax_conf['writerPassword']
        datax_json = json.dumps(datax_json)

    return {"datax": datax_json, "sql_ddl": ddl_json}

@router.get("/tools/excel/datax/get_datax_type")
def get_datax_type():
    """支持的datax 类型"""
    return {"datax_reader_type": [i.name for i in list(DataXReaderType)], "datax_writer_type": [i.name for i in list(DataXWriterType)]}

def _get_tables(df: pd.DataFrame) -> list:
    """
    获取sheet中所有的表
    :param df:
    :return:
    """
    table_list = df[['表名','表备注']].drop_duplicates().apply(lambda x: tuple(x), axis=1).values.tolist()
    return table_list

@router.get('/tools/db/download')
def download_template():
    # 假设模板文件名为 template.xlsx，位于服务器的某个路径下
    template_file_path = os.path.join(current_app.config['root_path'],"static/template/模板.xlsx")
    # 使用 Flask 的 send_file 函数发送文件
    return send_file(template_file_path, as_attachment=True)
