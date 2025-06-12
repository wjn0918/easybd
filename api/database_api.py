import urllib.parse
from fastapi import APIRouter,Query
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import PlainTextResponse,StreamingResponse

from easybd.db import PostgreSql, Mysql
from models.dbModel import ConnectionResponse, DBConfig, ExportRequest
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