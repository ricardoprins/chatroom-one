"""
At this point, all the endpoints are here...which is not the ideal.

/settings/controllers.py handles all the logic in the database,
pulling from /models, which will add dbinfo to MongoDB.
"""
import pymongo
import logging
from fastapi import FastAPI, WebSocket, Request, Depends
from fastapi.templating import Jinja2Templates
from settings import config
from settings.controllers import create_user, Notifier, insert_room
from settings.db import AsyncIOMotorClient, get_nosql_db, close_mongo_connection, connect_to_mongo
from fastapi.middleware.cors import CORSMiddleware
from schemas.users import RegisterRequest
from schemas.chatroom import RoomCreateRequest


app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
notifier = Notifier()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    client = await get_nosql_db()
    db = client[config.MONGODB_DBNAME]
    try:
        await notifier.generator.asend(None)
        await db.create_collection("users")
        await db.create_collection("rooms")
        await db.create_collection("messages")
        user_collection = db.users
        room_collection = db.rooms
        await user_collection.create_index("username", name="username", unique=True)
        await room_collection.create_index("room_name", name="room_name", unique=True)
    except pymongo.errors.CollectionInvalid as e:
        logging.info(e)
        pass


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.post('/register')
async def register_user(request: RegisterRequest, client: AsyncIOMotorClient = Depends(get_nosql_db)):
    try:
        db = client[config.MONGODB_DBNAME]
        collection = db.users
        res = create_user(request)
        return res
    except pymongo.errors.DuplicateKeyError as e:
        return {"error": e}


@app.post('/create_room')
async def create_room(request: RoomCreateRequest, client: AsyncIOMotorClient = Depends(get_nosql_db)):
    db = client[config.MONGODB_DBNAME]
    collection = db.rooms
    res = await insert_room(request.username, request.room_name, collection)
    return res
