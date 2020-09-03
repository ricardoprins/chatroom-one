from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from .users import UserInDB


class Message(BaseModel):
    user: UserInDB
    content: str = None


class MessageInDB(Message):
    _id: UUID = Field(default=uuid4)
    timestamp: datetime = Field(default=datetime.utcnow)
