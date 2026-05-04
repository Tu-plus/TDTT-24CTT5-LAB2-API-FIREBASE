from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.auth_dependency import get_current_user
import pyrebase
import json
import os

router = APIRouter()


# ── Login Schema ──
class LoginRequest(BaseModel):
    email: str
    password: str


def _get_pyrebase_auth():
    """Initialize pyrebase auth client for email/password login."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "firebase-web-config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        raise HTTPException(status_code=500, detail="Firebase web config not found")
    firebase = pyrebase.initialize_app(config)
    return firebase.auth()


@router.post("/login")
def login(req: LoginRequest):
    """Login with email/password and return Firebase ID token.
    
    Use the returned idToken in the Authorize button (Bearer token) to test other endpoints.
    """
    try:
        auth_client = _get_pyrebase_auth()
        result = auth_client.sign_in_with_email_and_password(req.email, req.password)
        return {
            "idToken": result["idToken"],
            "email": result.get("email"),
            "localId": result.get("localId"),
            "message": "Copy the idToken above, click Authorize 🔒, paste it as Bearer token."
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")


@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    """Return current user info from Firebase token."""
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "name": user.get("name", user.get("email", "User")),
        "picture": user.get("picture", None),
    }
