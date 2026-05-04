# ✅ TaskFlow — Ứng dụng Quản lý Công việc

> **Bài thực hành số 2 — API & Firebase**  
> Môn: Tư Duy Tính Toán · Trường ĐH Khoa Học Tự Nhiên TP.HCM  
> Giảng viên hướng dẫn: **Lê Đức Khoan**

Ứng dụng quản lý công việc (To-do App) với kiến trúc **Frontend – Backend** tách biệt, sử dụng **FastAPI**, **Streamlit**, **Firebase Authentication** và **Firestore Database**.

---

## 📑 Mục lục

- [Tính năng](#-tính-năng)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Thiết lập Firebase](#-thiết-lập-firebase)
- [Cài đặt môi trường](#-cài-đặt-môi-trường)
- [Chạy ứng dụng](#-chạy-ứng-dụng)
- [API Endpoints](#-api-endpoints)
- [Video Demo](#-video-demo)
- [Lưu ý bảo mật](#-lưu-ý-bảo-mật)

---

## ✨ Tính năng

### Xác thực (Authentication)
- 🔐 Đăng nhập bằng **Email/Password**
- 🔑 Đăng nhập bằng **Google** (OAuth 2.0)
- 📝 Đăng ký tài khoản mới
- 🚪 Đăng xuất
- 🍪 Tự động đăng nhập lại bằng Cookie

### Quản lý Task (Feature chính)
- ➕ **Thêm** task mới (tiêu đề, mô tả, mức độ ưu tiên, hạn chót)
- 📋 **Xem** danh sách task của người dùng hiện tại
- ✏️ **Sửa** task trực tiếp trên giao diện (inline editing)
- 🗑️ **Xoá** task
- ✅ **Đánh dấu** hoàn thành / bỏ hoàn thành
- 🚫 **Kiểm tra trùng** tiêu đề task

### Bộ lọc & Sắp xếp
- 🔍 Lọc theo trạng thái: Tất cả / Chưa xong / Hoàn thành
- 📊 Sắp xếp theo: Mức độ ưu tiên / Hạn chót gần nhất

### Giao diện
- 🎭 **2 theme màu sắc**: 🌙 Tối (Dark) · 🌊 Biển (Ocean Blue)
- 🌙 Dark theme hiện đại với hiệu ứng glassmorphism
- 📈 Dashboard thống kê: Tổng task / Hoàn thành / Còn lại
- 👤 User badge hiển thị tên và email
- 🎨 Priority badges với màu sắc phân biệt (🔴 Cao · 🟠 Trung bình · 🟢 Thấp)

---

## 🛠 Công nghệ sử dụng

| Thành phần | Công nghệ | Phiên bản |
|:-----------|:----------|:----------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | ≥ 0.115.0 |
| **Frontend** | [Streamlit](https://streamlit.io/) | ≥ 1.39.0 |
| **Authentication** | [Firebase Auth](https://firebase.google.com/docs/auth) | — |
| **Database** | [Cloud Firestore](https://firebase.google.com/docs/firestore) | — |
| **Server** | [Uvicorn](https://www.uvicorn.org/) (ASGI) | ≥ 0.30.6 |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) | ≥ 2.11.0 |
| **Firebase SDK** | firebase-admin (Backend) + Pyrebase4 (Frontend) | — |

---

## 📁 Cấu trúc thư mục

```
todo-app/
│
├── backend/                          # ── BACKEND (FastAPI) ──────────────────
│   ├── __init__.py                   # Đánh dấu thư mục là Python package
│   ├── main.py                       # Entry point — Khởi tạo FastAPI app,
│   │                                 #   CORS middleware, mount routers,
│   │                                 #   định nghĩa GET / và GET /health
│   ├── routers/                      # Định tuyến API (API Router)
│   │   ├── __init__.py
│   │   ├── auth.py                   # Router xác thực — GET /auth/me
│   │   │                             #   trả về thông tin user hiện tại
│   │   └── tasks.py                  # Router quản lý task — CRUD endpoints
│   │                                 #   POST, GET, PATCH, DELETE /tasks/
│   │                                 #   Kiểm tra trùng tiêu đề, phân quyền
│   ├── schemas/                      # Pydantic schema (data validation)
│   │   ├── __init__.py
│   │   └── task.py                   # TaskCreate, TaskUpdate schema
│   │                                 #   Enum Priority (low/medium/high)
│   └── services/                     # Tầng service / business logic
│       ├── __init__.py
│       ├── firebase_service.py       # Khởi tạo Firebase Admin SDK,
│       │                             #   Firestore client, verify ID token
│       └── auth_dependency.py        # FastAPI Dependency — xác thực Bearer
│                                     #   token cho các endpoint yêu cầu auth
│
├── frontend/                         # ── FRONTEND (Streamlit) ──────────────
│   ├── app.py                        # Entry point — Toàn bộ giao diện:
│   │                                 #   Login/Register, Dashboard, Task CRUD,
│   │                                 #   Filter/Sort, Stats, Theme Picker
│   ├── themes.py                     # Định nghĩa 2 theme (Dark, Ocean Blue)
│   │                                 #   và hàm generate CSS động theo theme
│   ├── auth_component/               # Streamlit Custom Component
│   │   └── index.html                # Giao diện nút "Đăng nhập bằng Google"
│   │                                 #   Sử dụng Firebase JS SDK (signInWithPopup)
│   ├── assets/                       # Tài nguyên tĩnh
│   │   ├── logo.png                  # Logo ứng dụng TaskFlow
│   │   └── favicon.png               # Favicon hiển thị trên tab trình duyệt
│   └── .streamlit/
│       └── config.toml               # Cấu hình Streamlit theme (dark mode)
│
├── requirements.txt                  # Danh sách thư viện Python cần cài
├── .env.example                      # Mẫu file biến môi trường
├── .gitignore                        # Loại trừ secrets, cache, venv khỏi Git
├── firebase-credentials.json         # 🔒 Service Account key (KHÔNG commit)
├── firebase-web-config.json          # 🔒 Firebase Web config (KHÔNG commit)
└── README.md                         # Tài liệu hướng dẫn (file này)
```

---

## 🔥 Thiết lập Firebase

### Bước 1: Tạo Firebase Project

1. Truy cập [Firebase Console](https://console.firebase.google.com)
2. Nhấn **"Add project"** → đặt tên project → tắt Google Analytics (nếu không cần) → **Create**

### Bước 2: Bật Authentication

1. Trong Firebase Console → **Authentication** → **Get started**
2. Tab **Sign-in method**:
   - Bật **Email/Password** → **Save**
   - Bật **Google** → điền email hỗ trợ → **Save**

### Bước 3: Tạo Firestore Database

1. Trong Firebase Console → **Firestore Database** → **Create database**
2. Chọn **Start in test mode** → **Next** → chọn region gần nhất → **Enable**

### Bước 4: Lấy Service Account Key (cho Backend)

1. Vào **Project Settings** (⚙️) → tab **Service accounts**
2. Nhấn **"Generate new private key"** → **Generate key**
3. Tải file JSON về → đổi tên thành `firebase-credentials.json`
4. Đặt vào **thư mục gốc** của project (`todo-app/`)

### Bước 5: Lấy Web Config (cho Frontend)

1. Vào **Project Settings** → tab **General** → kéo xuống **"Your apps"**
2. Nhấn **"Add app"** → chọn icon **Web (`</>`)**
3. Đặt tên app → **Register app**
4. Copy đoạn `firebaseConfig` và tạo file `firebase-web-config.json` ở thư mục gốc:

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

## ⚙️ Cài đặt môi trường

### Yêu cầu

- **Python** 3.10 – 3.12 (khuyến nghị)
- **pip** (Python package manager)

### Cài đặt

```bash
# 1. Clone repository
git clone <repo-url>
cd todo-app

# 2. Tạo virtual environment
python -m venv venv

# 3. Kích hoạt virtual environment
# ── Windows (PowerShell):
.\venv\Scripts\activate
# ── Windows (CMD):
venv\Scripts\activate
# ── macOS / Linux:
source venv/bin/activate

# 4. Cài đặt thư viện
pip install -r requirements.txt
```

### Cấu hình

Đặt 2 file Firebase vào thư mục gốc (xem phần [Thiết lập Firebase](#-thiết-lập-firebase)):

- `firebase-credentials.json` — Service Account key cho backend
- `firebase-web-config.json` — Web config cho frontend

> **Tùy chọn:** Có thể dùng biến môi trường thay vì file JSON. Xem file `.env.example` để biết chi tiết.

---

## 🚀 Chạy ứng dụng

### Chạy Backend

Mở terminal đầu tiên:

```bash
# Kích hoạt venv (nếu chưa)
.\venv\Scripts\activate          # Windows
source venv/bin/activate          # macOS/Linux

# Chạy server
cd backend
uvicorn main:app --reload --port 8000
```

- 🌐 Backend chạy tại: [http://localhost:8000](http://localhost:8000)
- 📖 API Docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Chạy Frontend

Mở terminal thứ hai:

```bash
# Kích hoạt venv (nếu chưa)
.\venv\Scripts\activate          # Windows
source venv/bin/activate          # macOS/Linux

# Chạy Streamlit
cd frontend
streamlit run app.py
```

- 🖥️ Frontend chạy tại: [http://localhost:8501](http://localhost:8501)

> **Lưu ý:** Đảm bảo Backend đang chạy trước khi mở Frontend.

---

## 📌 API Endpoints

### Endpoints công khai (không yêu cầu xác thực)

| Method | Endpoint | Mô tả | Response |
|:------:|:---------|:-------|:---------|
| `GET`  | `/`      | Kiểm tra API đang chạy | `{"message": "Todo App API is running"}` |
| `GET`  | `/health`| Health check | `{"status": "ok"}` |

### Endpoints xác thực (yêu cầu Bearer token)

| Method   | Endpoint        | Mô tả                           | Request Body |
|:--------:|:----------------|:---------------------------------|:-------------|
| `GET`    | `/auth/me`      | Lấy thông tin user hiện tại      | — |
| `POST`   | `/tasks/`       | Tạo task mới                     | `TaskCreate` |
| `GET`    | `/tasks/`       | Lấy danh sách task của user      | — |
| `PATCH`  | `/tasks/{id}`   | Cập nhật task (title, description, priority, deadline, completed) | `TaskUpdate` |
| `DELETE` | `/tasks/{id}`   | Xoá task                         | — |

### Schemas

**TaskCreate:**
```json
{
  "title": "string (bắt buộc)",
  "description": "string (tuỳ chọn)",
  "priority": "low | medium | high (mặc định: medium)",
  "deadline": "string ISO date (tuỳ chọn)"
}
```

**TaskUpdate:**
```json
{
  "title": "string (tuỳ chọn)",
  "description": "string (tuỳ chọn)",
  "priority": "low | medium | high (tuỳ chọn)",
  "completed": "boolean (tuỳ chọn)",
  "deadline": "string ISO date (tuỳ chọn)"
}
```

---

## 🎥 Video Demo

> [Đặt link video demo ở đây]

**Nội dung video demo bao gồm:**
1. Giới thiệu ứng dụng TaskFlow
2. Chạy Backend (FastAPI + Uvicorn)
3. Chạy Frontend (Streamlit)
4. Đăng nhập bằng Firebase (Email/Password hoặc Google)
5. Demo feature chính: Thêm / Xem / Sửa / Xoá / Đánh dấu hoàn thành task
6. Minh họa dữ liệu được lưu và đọc từ Firestore Database

---

## ⚠️ Lưu ý bảo mật

| File | Mô tả | Commit? |
|:-----|:-------|:-------:|
| `firebase-credentials.json` | Service Account private key | ❌ **KHÔNG** |
| `firebase-web-config.json` | Firebase Web config (chứa API key) | ❌ **KHÔNG** |
| `.env` | Biến môi trường cục bộ | ❌ **KHÔNG** |
| `.env.example` | Mẫu biến môi trường (không chứa secret) | ✅ Có |

Hai file Firebase đã được thêm vào `.gitignore`. Chỉ commit các file mẫu (`.env.example`) để người khác biết cấu trúc cần thiết.

---

## 📄 Thư viện sử dụng

| Thư viện | Mục đích |
|:---------|:---------|
| `fastapi` | Web framework cho backend API |
| `uvicorn` | ASGI server để chạy FastAPI |
| `firebase-admin` | Firebase Admin SDK — xác thực token, thao tác Firestore |
| `python-dotenv` | Đọc biến môi trường từ file `.env` |
| `pydantic` | Data validation & serialization |
| `requests` | HTTP client (frontend gọi backend API) |
| `streamlit` | Framework xây dựng giao diện web |
| `pillow` | Xử lý ảnh (logo, favicon) |
| `pyrebase4` | Firebase client SDK cho Python (đăng nhập email/password) |
| `streamlit-cookies-controller` | Quản lý cookies trong Streamlit (auto-login) |

---

<p align="center">
  <b>TaskFlow</b> · Built with ❤️ using FastAPI & Streamlit
</p>
