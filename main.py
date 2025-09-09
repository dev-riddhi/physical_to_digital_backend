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
        "*",
    ],
    allow_credentials=True,  # needed for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(guest)
app.include_router(user)
app.include_router(admin)
