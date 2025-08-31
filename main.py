from fastapi import FastAPI , APIRouter
from app.routes.auth_routes import auth

app = FastAPI()

app.include_router(auth)
