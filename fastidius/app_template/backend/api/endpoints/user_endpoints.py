from fastapi import APIRouter, Depends
from backend.models.user import UserDB
from backend.core.auth import current_active_user

router = APIRouter()


@router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
