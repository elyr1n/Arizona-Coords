from pydantic import BaseModel


class StaticIDSchema(BaseModel):
    id: int
    server: str


class CoordinatesSchema(BaseModel):
    nickname: str
    x: int
    y: int
    z: int


class KladSchema(BaseModel):
    nickname: str
    x: int
    y: int
    z: int
    loot: list[str]
    time: str
