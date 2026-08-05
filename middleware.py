from fastapi import HTTPException

from schemas import StaticIDSchema
from storage import static_ids


def verify_static_id(sid: StaticIDSchema):
    if (sid.id, sid.server) in static_ids:
        return True

    raise HTTPException(status_code=403, detail="Доступ запрещён!")
