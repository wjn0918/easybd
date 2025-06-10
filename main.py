from typing import Union

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

from db import create_db_and_tables

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

from api import config, tools,db,deploy_code,excel_api



@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


app.include_router(config.router)
app.include_router(tools.router)
app.include_router(db.router)
app.include_router(deploy_code.router)
app.include_router(excel_api.router)


