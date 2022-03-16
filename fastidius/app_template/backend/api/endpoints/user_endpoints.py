from fastapi import APIRouter, Depends
from models.user import UserDB
from core.auth import current_active_user

router = APIRouter()


@router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
