from typing import List, Literal

from pydantic import BaseModel


class JdbcModel(BaseModel):
    jdbcUrl: str
    userName: str
    passwd: str


class DDLModel(BaseModel):
    jdbInfo: JdbcModel
    ddl: str


# 请求参数模型
class DBConfig(BaseModel):
    dbType: Literal['pgsql', 'mysql']
    host: str
    port: int
    username: str
    password: str
    database: str

# 响应模型
class ConnectionResponse(BaseModel):
    success: bool
    tables: List[str] = []
    message: str = ""

class ExportRequest(BaseModel):
    dbType: str  # 'pgsql' or 'mysql'
    host: str
    port: int
    username: str
    password: str
    database: str
    tables: List[str]

class SyncTarget(BaseModel):
    source: dict
    target: dict