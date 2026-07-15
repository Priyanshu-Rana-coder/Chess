from fastapi import APIRouter, WebSocket
from User.auth import verify_token
from room_page.room_manager import MANAGER
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, token: str):
    await websocket.accept()

    payload = verify_token(token)
    if payload is None:
        await websocket.close()
        return

    room = MANAGER.get_room(room_id)
    if room is None:
        await websocket.close()
        return

    username = payload["username"]

    if room.white["username"] == username:
        room.white_socket = websocket
        print("White connected")

    elif room.black["username"] == username:
        room.black_socket = websocket
        print("Black connected")

    else:
        await websocket.close()
        return

    await websocket.send_json({
        "type": "connected"
    })
    try:
        while True:
            data = await websocket.receive_json()

            if websocket == room.white_socket:
                if room.black_socket is not None:
                    await room.black_socket.send_json(data)

            elif websocket == room.black_socket:
                if room.white_socket is not None:
                    await room.white_socket.send_json(data)
    except WebSocketDisconnect:
        print(f"{username} disconnected")