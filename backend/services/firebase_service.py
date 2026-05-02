import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

_app = None
_db = None


def get_firebase_app():
    global _app
    if _app is None:
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        if not cred_path:
            # Look in the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            cred_path = os.path.join(project_root, "firebase-credentials.json")
            if not os.path.exists(cred_path):
                cred_path = "firebase-credentials.json"
        cred = credentials.Certificate(cred_path)
        _app = firebase_admin.initialize_app(cred)
    return _app


def get_db():
    global _db
    if _db is None:
        get_firebase_app()
        _db = firestore.client()
    return _db


def verify_token(id_token: str) -> dict:
    """Verify Firebase ID token and return decoded token."""
    get_firebase_app()
    decoded = auth.verify_id_token(id_token)
    return decoded
