from typing import Union, Annotated
from fastapi import Depends
from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class ConfigModel(SQLModel, table=True):
    id: str= Field(default=None, primary_key=True)
    confType: str = Field()
    confName: str = Field()
    confContent: str = Field()


class ConfigModelUpdate(BaseModel):
    confContent: str = Field()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
