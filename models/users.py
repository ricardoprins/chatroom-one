from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class User(BaseModel):
    username: str
    hashed_password: str
    salt: str


class UserInDB(User):
    _id: UUID = Field(default=uuid4)
    date_created: datetime = Field(default=datetime.utcnow)
