import uuid

from fastapi import APIRouter, HTTPException

from db import SessionDep, select, ConfigModel, ConfigModelUpdate
from models.config import ConfigCreate

router = APIRouter(prefix="/api/config", tags=["config"])


@router.post("/create")
def conf_create(conf_create:ConfigCreate, session: SessionDep):
    conf = ConfigModel(
        **conf_create.dict()
    )
    session.add(conf)
    session.commit()
    session.refresh(conf)
    return {"message": "创建成功"}



@router.get("/select")
def conf_select(session: SessionDep):
    c = session.exec(select(ConfigModel)).all()
    return c


@router.get("/select/{conf_type}")
def conf_select_by_conf_type(conf_type, session: SessionDep):

    config_mytools = session.exec(select(ConfigModel).where(ConfigModel.confType == conf_type)).all()
    return config_mytools


@router.delete('/{id}')
def conf_delete(id, session: SessionDep):
    confdel = session.get(ConfigModel, id)
    if not confdel:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(confdel)
    session.commit()
    return {"ok": True}
#
#
@router.post('/update/{id}')
def conf_update(id, update_model:ConfigModelUpdate, session: SessionDep):
    print(update_model)
    conf_model = session.get(ConfigModel, id)
    if not conf_model:
        raise HTTPException(status_code=404, detail="Hero not found")
    conf_model.sqlmodel_update(update_model)
    session.add(conf_model)
    session.commit()
    session.refresh(conf_model)
    return {"message": "更新成功"}

