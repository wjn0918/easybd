import uuid

from fastapi import APIRouter, HTTPException

from db import SessionDep, select, ConfigModel, ConfigModelUpdate
from models.dbModel import DDLModel

router = APIRouter(prefix="/api/tools/db", tags=["tools"])



@router.post("/execddl")
def exec_ddl(conf:DDLModel, session: SessionDep):
    print(conf)

