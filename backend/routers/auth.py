from fastapi import APIRouter, Depends
from services.auth_dependency import get_current_user

router = APIRouter()


@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    """Return current user info from Firebase token."""
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "name": user.get("name", user.get("email", "User")),
        "picture": user.get("picture", None),
    }
