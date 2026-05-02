# ✅ TaskFlow — To-do App

Ứng dụng quản lý công việc với **FastAPI** backend, **Streamlit** frontend, **Firebase Authentication** và **Firestore** database.

---

## 📁 Cấu trúc dự án

```
todo-app/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── schemas/
│   │   └── task.py
│   └── services/
│       ├── firebase_service.py
│       └── auth_dependency.py
├── frontend/
│   └── app.py
├── requirements.txt
├── .gitignore
├── firebase-credentials.example.json   ← mẫu (không commit file thật)
└── firebase-web-config.example.json    ← mẫu (không commit file thật)
```

---

## 🔥 Bước 1: Tạo Firebase Project

### 1.1 Tạo project
1. Vào [https://console.firebase.google.com](https://console.firebase.google.com)
2. Nhấn **"Add project"** → đặt tên → tắt Google Analytics nếu không cần → **Create**

### 1.2 Bật Authentication
1. Trong Firebase Console → **Authentication** → **Get started**
2. Chọn tab **Sign-in method** → chọn **Email/Password** → bật **Enable** → **Save**

### 1.3 Tạo Firestore Database
1. Trong Firebase Console → **Firestore Database** → **Create database**
2. Chọn **Start in test mode** (cho phép đọc/ghi tự do trong 30 ngày) → **Next** → chọn region → **Enable**

### 1.4 Lấy Service Account (dùng cho backend)
1. Vào **Project Settings** (biểu tượng ⚙️) → tab **Service accounts**
2. Nhấn **"Generate new private key"** → **Generate key** → tải về file JSON
3. Đổi tên thành `firebase-credentials.json` → đặt vào thư mục gốc của project

### 1.5 Lấy Web Config (dùng cho frontend)
1. Vào **Project Settings** → tab **General** → kéo xuống phần **"Your apps"**
2. Nhấn **"Add app"** → chọn icon **Web (`</>`)**
3. Đặt tên app → **Register app**
4. Copy đoạn `firebaseConfig` (gồm apiKey, authDomain, v.v.)
5. Tạo file `firebase-web-config.json` ở thư mục gốc theo mẫu:

```json
{
  "apiKey": "AIza...",
  "authDomain": "your-project.firebaseapp.com",
  "projectId": "your-project-id",
  "storageBucket": "your-project.appspot.com",
  "messagingSenderId": "123456789",
  "appId": "1:123:web:abc",
  "databaseURL": ""
}
```

---

## ⚙️ Bước 2: Cài đặt môi trường

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (macOS/Linux)
source venv/bin/activate

# Cài thư viện
pip install -r requirements.txt
```

---

## 🚀 Bước 3: Chạy Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend sẽ chạy tại: [http://localhost:8000](http://localhost:8000)  
API docs tại: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🎨 Bước 4: Chạy Frontend

Mở terminal mới:

Trên Windows:
```bash
.\venv\Scripts\activate
```

Trên macOS/Linux:
```bash
source venv/bin/activate
```
Đảm bảo bạn thấy chữ (venv) xuất hiện ở đầu dòng lệnh

```bash
cd frontend
streamlit run app.py
```

Frontend sẽ chạy tại: [http://localhost:8501](http://localhost:8501)

---

## 📌 Các API Endpoint

| Method | Endpoint       | Mô tả                        | Auth |
|--------|----------------|------------------------------|------|
| GET    | `/`            | Kiểm tra API                 | ❌   |
| GET    | `/health`      | Health check                 | ❌   |
| GET    | `/auth/me`     | Thông tin user hiện tại      | ✅   |
| POST   | `/tasks/`      | Tạo task mới                 | ✅   |
| GET    | `/tasks/`      | Lấy danh sách task           | ✅   |
| PATCH  | `/tasks/{id}`  | Cập nhật task                | ✅   |
| DELETE | `/tasks/{id}`  | Xoá task                     | ✅   |

---

## 🎥 Video Demo

> [Đặt link video demo ở đây]

---

## ⚠️ Lưu ý bảo mật

- **KHÔNG** commit `firebase-credentials.json` và `firebase-web-config.json` lên GitHub
- Hai file này đã được thêm vào `.gitignore`
- Chỉ commit các file `.example.json` làm mẫu
