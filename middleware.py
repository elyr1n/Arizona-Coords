from fastapi import HTTPException

from schemas import StaticIDSchema
from storage import static_ids


def verify_static_id(sid: StaticIDSchema):
    for value in static_ids:
        if value["id"] == sid.id and value["server"] == sid.server:
            return True

    raise HTTPException(status_code=403, detail="Доступ запрещён!")
