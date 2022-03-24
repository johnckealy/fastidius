from fastapi import Depends, FastAPI
from typing import List, Any
from fastapi.middleware.cors import CORSMiddleware

from backend.db import create_db_and_tables
% if auth:
from backend.core.auth import auth_backend, fastapi_users
from backend.api.endpoints.user_endpoints import router as user_routes
% endif

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
% if alembic:
    await create_db_and_tables()
% else:
    pass
% endif




% if auth:
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
app.include_router(user_routes)
% endif
