from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import auth
from app.routes.guest_routes import guest
from app.routes.user_routes import user
from app.routes.admin_routes import admin

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",  # sometimes you hit backend from this
    ],  # React dev server
    allow_credentials=True,  # needed for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(guest)
app.include_router(user)
app.include_router(admin)
