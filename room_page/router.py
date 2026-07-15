from fastapi import APIRouter, Depends, HTTPException
from User.auth import get_current_user
from .room_manager import RoomManager, MANAGER
from .schema import JoinRoomRequest
router = APIRouter(prefix="/room",tags=["Room"])


@router.post("/create")
def create_room(user=Depends(get_current_user)):
    room=MANAGER.create_room(user)
    return {"room_id": room.room_id}


@router.post("/join")
def join_room(request: JoinRoomRequest,user=Depends(get_current_user)):
    room = MANAGER.join_room(user, request.room_id)
    if room is None:
        raise HTTPException(status_code=404,detail="Room not found")
    if room == "full":
        raise HTTPException(status_code=409,detail="Room already full")
    return {"room_id": room.room_id}