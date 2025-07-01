import os
import re
import shutil
import sqlite3
import tempfile
import urllib.parse
from fastapi import APIRouter,Query
from sqlalchemy import create_engine, inspect,text
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import PlainTextResponse,StreamingResponse,FileResponse
from starlette.background import BackgroundTask

from easybd.db import PostgreSql, Mysql, BaseDB
from models.dbModel import ConnectionResponse, DBConfig, ExportRequest, SyncTarget
from fastapi import FastAPI, HTTPException

router = APIRouter(prefix="/api/database", tags=["database"])

@router.post("/test-connection", response_model=ConnectionResponse)
def connection_test(config: DBConfig):
    # 构建连接 URL
    password = urllib.parse.quote_plus(config.password)
    if config.dbType == "pgsql":
        url = f"postgresql://{config.username}:{password}@{config.host}:{config.port}/{config.database}"
    elif config.dbType == "mysql":
        url = f"mysql+pymysql://{config.username}:{password}@{config.host}:{config.port}/{config.database}"
    else:
        raise HTTPException(status_code=400, detail="Unsupported database type")

    try:
        engine = create_engine(url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return ConnectionResponse(success=True, tables=tables)
    except SQLAlchemyError as e:
        return ConnectionResponse(success=False, message=str(e.__cause__ or e))


@router.post("/export-table-structure")
async def export_table_structure(req: ExportRequest):
    if req.dbType == "pgsql":
        pg = PostgreSql(req.host, req.port, req.username, req.password, req.database, "public",table_names=req.tables)
        output = pg.table_info_to_excel_io()
        headers = {
            "Content-Disposition": 'attachment; filename="export.xlsx"'
        }
        return StreamingResponse(output,
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers=headers)
    if req.dbType == "mysql":
        mysql = Mysql(req.host, req.port, req.username, req.password, req.database,table_names=req.tables)
        output = mysql.table_info_to_excel_io()
        headers = {
            "Content-Disposition": 'attachment; filename="export.xlsx"'
        }
        return StreamingResponse(output,
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers=headers)
    else:
        raise HTTPException(status_code=400, detail="Unsupported database type")



def map_to_sqlite_type(col_type: str) -> str:
    col_type = re.sub(r'\(.*\)', '', col_type).strip().lower()
    if col_type in ("int", "integer", "bigint", "smallint", "tinyint"):
        return "INTEGER"
    elif col_type in ("float", "double", "decimal", "numeric", "real"):
        return "REAL"
    elif col_type in ("bool", "boolean"):
        return "INTEGER"
    elif col_type in ("date", "datetime", "timestamp"):
        return "TEXT"
    elif col_type in ("text", "varchar", "char", "string", "json"):
        return "TEXT"
    else:
        return "TEXT"  # fallback

@router.post("/convert-to-sqlite")
async def export_table_structure(req: ExportRequest):
    baseDB: BaseDB = None
    if req.dbType == "pgsql":
        baseDB = PostgreSql(req.host, req.port, req.username, req.password, req.database, "public",table_names=req.tables)
    if req.dbType == "mysql":
        baseDB = Mysql(req.host, req.port, req.username, req.password, req.database,table_names=req.tables)
    else:
        raise HTTPException(status_code=400, detail="Unsupported database type")
    src_engine = baseDB.engine
    col_info = baseDB.table_info['table_cols'].to_list()

    # 创建临时 SQLite 文件
    tmpdir = tempfile.mkdtemp()
    sqlite_path = os.path.join(tmpdir, 'converted.sqlite')
    try:
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()

        with src_engine.connect() as conn:
            for i, table in enumerate(req.tables):
                columns_info = col_info[i]
                column_defs = ", ".join(
                    f'"{col["col_name"]}" {map_to_sqlite_type(col["col_type"])}'
                    for col in columns_info
                )
                sqlite_cursor.execute(f'CREATE TABLE {table} ({column_defs})')

                # 插入数据
                rows = conn.execute(text(f'SELECT * FROM {table}')).fetchall()
                if rows:
                    placeholders = ", ".join(["?"] * len(columns_info))
                    sqlite_cursor.executemany(
                        f'INSERT INTO "{table}" VALUES ({placeholders})',
                        [tuple(map(str, row)) for row in rows]
                    )
        sqlite_conn.commit()
        sqlite_conn.close()

        return FileResponse(
            path=sqlite_path,
            filename="converted.sqlite",
            media_type='application/octet-stream',
            background=BackgroundTask(shutil.rmtree, tmpdir, ignore_errors=True)
        )

    except Exception as e:
        print(e)
        shutil.rmtree(tmpdir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")


@router.post("/sync2target")
async def sync2target(req: SyncTarget):
    source_conf = req.source
    target_conf = req.target
    baseDB: BaseDB = None

    s_dbtype = source_conf['dbType']
    s_host = source_conf['host']
    s_port = source_conf['port']
    s_username = source_conf['username']
    s_password = source_conf['password']
    s_database = source_conf['database']
    print(source_conf)
    print(s_database)
    s_tables = source_conf['tables']
    if s_dbtype == "pgsql":
        baseDB = PostgreSql(s_host, s_port, s_username, s_password, s_database, "public",
                            table_names=s_tables)
    # if s_dbtype == "mysql":
    #     baseDB = Mysql(s_host, s_port, s_username, s_password, s_database, table_names=s_tables)
    # else:
    #     raise HTTPException(status_code=400, detail="Unsupported database type")
    for t in s_tables:
        baseDB.sync_clickhouse_table(target_conf, t)


    return {"message": "同步成功"}
    # if req.dbType == "pgsql":
    #     pg = PostgreSql(req.host, req.port, req.username, req.password, req.database, "public",table_names=req.tables)
    #     output = pg.table_info_to_excel_io()
    #     headers = {
    #         "Content-Disposition": 'attachment; filename="export.xlsx"'
    #     }
    #     return StreamingResponse(output,
    #                              media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #                              headers=headers)
    # if req.dbType == "mysql":
    #     mysql = Mysql(req.host, req.port, req.username, req.password, req.database,table_names=req.tables)
    #     output = mysql.table_info_to_excel_io()
    #     headers = {
    #         "Content-Disposition": 'attachment; filename="export.xlsx"'
    #     }
    #     return StreamingResponse(output,
    #                              media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #                              headers=headers)
    # else:
    #     raise HTTPException(status_code=400, detail="Unsupported database type")