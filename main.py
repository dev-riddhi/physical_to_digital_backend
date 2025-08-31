from fastapi import FastAPI 

from app.routers.auth import auth

app = FastAPI()

app.include_router(auth)