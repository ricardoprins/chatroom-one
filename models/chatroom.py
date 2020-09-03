from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from .users import UserInDB
from .messages import MessageInDB


class Chatroom(BaseModel):
    room_name: str
    members: Optional[List[UserInDB]]
    messages: Optional[List[MessageInDB]]
    last_pinged: datetime = Field(default=datetime.utcnow)


class ChatroomInDB(Chatroom):
    _id: UUID = Field(default=uuid4)
    date_created: datetime = Field(default=datetime.utcnow)
