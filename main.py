from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount('/assets', StaticFiles(directory='templates/assets'), name='assets')
templates = Jinja2Templates(directory='templates')


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
        await websocket.send_text(f"Message text was: {data}")
