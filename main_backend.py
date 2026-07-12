from fastapi import FastAPI, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from User.database import get_db
from User.schemas import LoginRequest, UserResponse
from User.crud import login_user
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

@app.post("/login", response_model=UserResponse)
def login(request: LoginRequest,db: Session = Depends(get_db)):
    user = login_user(
        db,
        request.username,
        request.password
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    return UserResponse(
        username=user.username,
        wins=user.wins,
        losses=user.losses,
        draws=user.draws
    )