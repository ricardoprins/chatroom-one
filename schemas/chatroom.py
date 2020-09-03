from pydantic import BaseModel


class RoomCreateRequest(BaseModel):
    username: str
    room_name: str
