from fastapi import APIRouter, Depends
from backend.models.user import UserDB
from backend.core.auth import current_active_user

router = APIRouter()


@router.get("/authentication-check")
async def authentication_check(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
