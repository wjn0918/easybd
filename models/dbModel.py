from typing import Optional

from pydantic import BaseModel


class JdbcModel(BaseModel):
    jdbcUrl: str
    userName: str
    passwd: str


class DDLModel(BaseModel):
    jdbInfo: JdbcModel
    ddl: str
