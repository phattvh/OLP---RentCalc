# Hướng dẫn cài đặt và chạy RentCalc từ mã nguồn

Dự án RentCalc được thiết kế để có thể cài đặt và triển khai sạch sẽ, nhanh chóng trên mọi hệ điều hành (Windows, Linux, macOS).

---

## 1. Yêu cầu hệ thống

- Python: Phiên bản 3.12 trở lên.
- Docker & Docker Compose: Chạy PostgreSQL 16.
- Git: Quản lý mã nguồn.

---

## 2. Các bước khởi chạy

### Bước 1: Clone mã nguồn và cài đặt môi trường

```bash
git clone https://github.com/phattvh/RentCalc.git
cd RentCalc

# Tạo và kích hoạt môi trường ảo
python -m venv .venv

# Trên Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Trên Linux/macOS:
source .venv/bin/activate

# Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt
```

### Bước 2: Khởi động cơ sở dữ liệu PostgreSQL bằng Docker

```bash
docker compose up -d db
```

### Bước 3: Áp dụng lược đồ Database và nạp dữ liệu Demo mẫu

```bash
# Tạo file môi trường cấu hình (nếu chưa có)
cp .env.example .env

# Chạy di chuyển lược đồ database lên phiên bản mới nhất
alembic upgrade head

# Nạp dữ liệu demo ban đầu (cơ sở, phòng trọ, công tơ, hóa đơn và tài khoản người dùng)
python scripts/seed.py
```

### Bước 4: Chạy ứng dụng Web

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Truy cập hệ thống tại: **http://localhost:8000**

---

## 3. Tài khoản Demo kiểm thử phân quyền (Role-Based Access)

Hệ thống đã nạp sẵn 2 tài khoản mẫu phục vụ chấm thi và nghiệm thu:

| Vai trò | Tên đăng nhập (`username`) | Mật khẩu (`password`) | Quyền hạn truy cập |
| :--- | :--- | :--- | :--- |
| **Chủ nhà (Owner)** | `owner` | `owner123` | Toàn quyền: Bảng điều khiển quản trị, thêm cơ sở, quản lý phòng, ghi chỉ số, phát hành hóa đơn, cấu hình biểu giá. |
| **Khách thuê (Tenant)** | `tenant101` | `tenant123` | Quyền giới hạn: Tự động chuyển hướng tới `/my-invoices`, chỉ xem được danh sách hóa đơn của riêng phòng 101, xem chi tiết và tải PDF. |

Trang đăng nhập: **http://localhost:8000/login**  
Trang đăng xuất: **http://localhost:8000/logout**

---

## 4. Chạy bộ kiểm thử tự động (Automated Test Suite)

Quy trình chuẩn hóa để chạy kiểm thử trên máy sạch từ mã nguồn:

```bash
# 1. Đảm bảo dịch vụ PostgreSQL đang chạy
docker compose up -d db

# 2. Cập nhật schema CSDL lên bản mới nhất
alembic upgrade head

# 3. Nạp dữ liệu mẫu phục vụ kiểm thử tích hợp
python -m scripts.seed

# 4. Thực thi toàn bộ 60 ca kiểm thử và xuất báo cáo độ bao phủ
pytest --cov=app --cov-report=term-missing
```

- Tiêu chuẩn nghiệm thu: **60/60 tests pass 100%**, Coverage $\ge$ 85%.
