from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from User.auth import verify_token
from room_page.room_manager import MANAGER
from User.database import SessionLocal
from User.models import User
import asyncio
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
    elif room.black["username"] == username:
        room.black_socket = websocket
    else:
        await websocket.close()
        return

    await websocket.send_json({"type": "connected"})

    db = SessionLocal()

    try:
        while True:
            data = await websocket.receive_json()
            if room.finished:
                continue

            if "resign" in data:
                room.finished = True

                if username == room.white["username"]:
                    winner = room.black["username"]
                    loser = room.white["username"]
                else:
                    winner = room.white["username"]
                    loser = room.black["username"]

                winner_user = db.query(User).filter(User.username == winner).first()
                loser_user = db.query(User).filter(User.username == loser).first()

                winner_user.wins += 1
                loser_user.losses += 1

                db.commit()

                if room.white_socket is not None:
                    await room.white_socket.send_json({"type": "resign", "winner": winner})

                if room.black_socket is not None:
                    await room.black_socket.send_json({"type": "resign", "winner": winner})

                await asyncio.sleep(0.3)

                MANAGER.delete_room(room.room_id)
                return
            if len(room.draw_requests) == 2:
                room.finished = True

                white_user = db.query(User).filter(User.username == room.white["username"]).first()
                black_user = db.query(User).filter(User.username == room.black["username"]).first()

                white_user.draws += 1
                black_user.draws += 1

                db.commit()

                if room.white_socket is not None:
                    await room.white_socket.send_json({"type": "draw"})

                if room.black_socket is not None:
                    await room.black_socket.send_json({"type": "draw"})

                await asyncio.sleep(0.3)

                MANAGER.delete_room(room.room_id)
                return

                if username == room.white["username"]:
                    opponent = room.black_socket
                else:
                    opponent = room.white_socket

                if opponent is not None:
                    await opponent.send_json({"type": "draw_offer"})

                continue

            if room.game.white_turn and websocket != room.white_socket:
                continue

            if (not room.game.white_turn) and websocket != room.black_socket:
                continue

            response = room.game.move(data["from"][0], data["from"][1], data["to"][0], data["to"][1])

            if response.success:
                room.draw_requests.clear()

            if room.white_socket is not None:
                await room.white_socket.send_json(response.model_dump())

            if room.black_socket is not None:
                await room.black_socket.send_json(response.model_dump())

            if response.checkmate:
                room.finished = True
                if room.game.white_turn:
                    winner = room.black["username"]
                    loser = room.white["username"]
                else:
                    winner = room.white["username"]
                    loser = room.black["username"]
                winner_user = db.query(User).filter(User.username == winner).first()
                loser_user = db.query(User).filter(User.username == loser).first()
                winner_user.wins += 1
                loser_user.losses += 1
                db.commit()
                await asyncio.sleep(0.3)

                MANAGER.delete_room(room.room_id)
                return

            elif response.stalemate:
                room.finished = True

                white_user = db.query(User).filter(User.username == room.white["username"]).first()
                black_user = db.query(User).filter(User.username == room.black["username"]).first()

                white_user.draws += 1
                black_user.draws += 1

                db.commit()

                await asyncio.sleep(0.3)

                MANAGER.delete_room(room.room_id)
                return

    except WebSocketDisconnect:
        if room.finished:
            return
        room.finished = True

        if room.white_socket == websocket:
            room.white_socket = None
            winner = room.black["username"]
            loser = room.white["username"]
        elif room.black_socket == websocket:
            room.black_socket = None
            winner = room.white["username"]
            loser = room.black["username"]
        winner_user = db.query(User).filter(User.username == winner).first()
        loser_user = db.query(User).filter(User.username == loser).first()
        winner_user.wins += 1
        loser_user.losses += 1
        db.commit()
        MANAGER.delete_room(room.room_id)
    finally:
        db.close()