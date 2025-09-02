from fastapi import FastAPI
from app.routes.auth_routes import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite default port
        "http://127.0.0.1:5173",   # sometimes you hit backend from this
    ],  # React dev server
    allow_credentials=True,                   # needed for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
