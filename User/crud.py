from sqlalchemy.orm import Session
from .models import User
from .auth import hash_password, verify_password
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str):
    user = User(
        username=username,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if user is None:
        return create_user(db, username, password)
    if verify_password(password, user.password_hash):
        return user
    return None

def add_win(db: Session, username: str):
    user = get_user(db, username)
    if user:
        user.wins += 1
        db.commit()

def add_loss(db: Session, username: str):
    user = get_user(db, username)
    if user:
        user.losses += 1
        db.commit()

def add_draw(db: Session, username: str):
    user = get_user(db, username)
    if user:
        user.draws += 1
        db.commit()

def get_stats(db: Session, username: str):
    user = get_user(db, username)
    if user is None:
        return None
    return {
        "username": user.username,
        "wins": user.wins,
        "losses": user.losses,
        "draws": user.draws
    }