from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import LoginRequest, UserResponse
from .crud import login_user
from .auth import create_access_token
router = APIRouter(prefix="/user",tags=["User"])

@router.post("/login", response_model=UserResponse)
def login(request: LoginRequest,db: Session = Depends(get_db)):
    user = login_user(db,request.username,request.password)
    if user is None:
        raise HTTPException(status_code=401,detail="Incorrect password")
    token = create_access_token({"username":user.username})
    return UserResponse(username=user.username,wins=user.wins,losses=user.losses,draws=user.draws,token=token)