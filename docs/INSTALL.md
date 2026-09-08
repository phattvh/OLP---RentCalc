# Hướng dẫn cài đặt và chạy RentCalc từ mã nguồn

Dự án RentCalc được thiết kế để có thể cài đặt và triển khai sạch sẽ, nhanh chóng trên mọi hệ điều hành.

---

## 1. Yêu cầu hệ thống

- Python: Phiên bản 3.12 trở lên.
- Docker & Docker Compose: Chạy PostgreSQL 16.
- Git: Quản lý mã nguồn.

---

## 2. Các bước khởi chạy

### Bước 1: Clone mã nguồn và cài đặt thư viện

```bash
git clone https://github.com/phattvh/RentCalc.git
cd RentCalc

python -m venv .venv
# Trên Windows:
.venv\Scripts\Activate.ps1
# Trên Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Bước 2: Chạy PostgreSQL bằng Docker

```bash
docker compose up -d db
```

### Bước 3: Di chuyển lược đồ và nạp dữ liệu mẫu

```bash
cp .env.example .env
alembic upgrade head
python scripts/seed.py
```

### Bước 4: Chạy ứng dụng Web

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Truy cập: http://localhost:8000
