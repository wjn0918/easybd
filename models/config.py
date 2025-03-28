from sqlmodel import SQLModel, Field


class DBConfigModel(SQLModel):
    confType: str = Field()
    confName: str = Field()
    confContent: str = Field()
