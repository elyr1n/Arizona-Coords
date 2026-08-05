from fastapi import FastAPI

from sqlalchemy import select

from storage import coords
from schemas import StaticIDSchema, CoordinatesSchema, KladSchema
from middleware import verify_static_id
from database import async_session_maker, KladModel, setup_database, SessionDep

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
    title="Arizona-Coords",
)


@app.get("/")
def root():
    return {"status": True, "message": "API работает!"}


@app.post("/static")
def check_static(sid: StaticIDSchema):
    verify_static_id(sid)

    return {"status": True, "message": "Доступ разрешён!"}


@app.post("/coords")
def set_coordinates(sid: StaticIDSchema, coordinates: CoordinatesSchema):
    verify_static_id(sid)

    coords["nickname"] = coordinates.nickname
    coords["x"] = coordinates.x
    coords["y"] = coordinates.y
    coords["z"] = coordinates.z

    return {
        "success": True,
        "nickname": coords["nickname"],
        "x": coords["x"],
        "y": coords["y"],
        "z": coords["z"],
    }


@app.get("/coords")
def get_coordinates(id: int, server: str):
    sid = StaticIDSchema(id=id, server=server)
    verify_static_id(sid)

    return {
        "success": True,
        "nickname": coords["nickname"],
        "x": coords["x"],
        "y": coords["y"],
        "z": coords["z"],
    }


@app.post("/klad", status_code=201)
async def add_klad(sid: StaticIDSchema, klad: KladSchema):
    verify_static_id(sid)

    async with async_session_maker() as session:
        new_klad = KladModel(
            nickname=klad.nickname,
            x=klad.x,
            y=klad.y,
            z=klad.z,
            loot=klad.loot,
            time=klad.time,
        )

        session.add(new_klad)
        await session.commit()

    return {"success": True, "message": "Клад добавлен!"}


@app.get("/klad")
async def get_klads(id: int, server: str, session: SessionDep):
    sid = StaticIDSchema(id=id, server=server)
    verify_static_id(sid)

    result = await session.execute(select(KladModel))

    klads = result.scalars().all()

    return {
        "success": True,
        "klads": [
            {
                "id": klad.id,
                "nickname": klad.nickname,
                "x": klad.x,
                "y": klad.y,
                "z": klad.z,
                "loot": klad.loot,
                "time": klad.time,
            }
            for klad in klads
        ],
    }
