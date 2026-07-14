from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from User.database import Base, engine
from User import models
from User.router import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3002",
        "http://localhost:3002",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)