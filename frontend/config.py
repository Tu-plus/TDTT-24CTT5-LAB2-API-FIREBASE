import os
import json

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def load_firebase_config():
    # Giả sử file config nằm ở thư mục gốc của dự án
    config_path = os.path.join(os.path.dirname(__file__), "..", "firebase-web-config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    
    # Fallback: đọc từ biến môi trường
    return {
        "apiKey":            os.getenv("FIREBASE_API_KEY", ""),
        "authDomain":        os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId":         os.getenv("FIREBASE_PROJECT_ID", ""),
        "storageBucket":     os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId":             os.getenv("FIREBASE_APP_ID", ""),
        "databaseURL":       "",
    }
