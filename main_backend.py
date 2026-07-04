from fastapi import FastAPI, WebSocket
from act import Game
from rooms import Room
app=FastAPI()
rooms={}
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data=await websocket.receive_json()
        room_id=data["room"]
        if room_id not in rooms:
            await websocket.send_json({"didMove": False,"message": "Room does not exist."})
            continue
        room=rooms[room_id]
        response=room.game.move(
            data["x1"],
            data["y1"],
            data["x2"],
            data["y2"]
        )
        await websocket.send_json(response)