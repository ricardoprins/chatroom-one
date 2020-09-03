import hashlib
import uuid
from collections import defaultdict
from models.users import UserInDB
from settings.db import get_nosql_db
from settings.config import MONGODB_DBNAME
from models.chatroom import ChatroomInDB


class Notifier:
    def __init__(self):
        self.connections: dict = defaultdict(dict)
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            print(f"MESSAGE : {message}")
            msg = message["message"]
            room_name = message["room_name"]
            await self._notify(msg, room_name)

    async def push(self, msg: str, room_name: str = None):
        message_body = {"message": msg, "room_name": room_name}
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if self.connections[room_name] == {} or len(self.connections[room_name]) == 0:
            self.connections[room_name] = []
        self.connections[room_name].append(websocket)
        print(f"CONNECTIONS : {self.connections[room_name]}")

    def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)

    async def _notify(self, message: str, room_name: str):
        living_connections = []
        while len(self.connections[room_name]) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections[room_name].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections[room_name] = living_connections


async def create_user(request, collection):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(
        request.password.encode("utf-8") + salt.encode("utf-8")).hexdigest()

    user = {}
    user['username'] = request.username
    user['salt'] = salt
    user['hashed_password'] = hashed_password
    dbuser = UserInDB(**user)
    response = await collection.insert_one(dbuser.dict())
    return {"id_inserted": str(response.inserted_id)}


async def get_user(name) -> UserInDB:
    client = await get_nosql_db()
    db = client[MONGODB_DBNAME]
    collection = db.users
    row = await collection.find_one({"username": name})
    if row is not None:
        return UserInDB(**row)
    else:
        return None


async def insert_room(username, room_name, collection):
    room = {}
    room["room_name"] = room_name
    user = await get_user(username)
    room["members"] = [user] if user is not None else []
    dbroom = ChatroomInDB(**room)
    response = await collection.insert_one(dbroom.dict())
    return {"id_inserted": str(response.inserted_id)}
