# Hướng dẫn triển khai Production (Production Deployment Guide)

Tài liệu hướng dẫn triển khai ứng dụng RentCalc lên máy chủ sản xuất sử dụng Docker, Docker Compose và Nginx.

---

## 1. Yêu cầu hệ thống (Prerequisites)
- **Hệ điều hành:** Ubuntu 22.04 LTS hoặc Linux tương đương
- **Docker Engine:** Phiên bản 24.0+
- **Docker Compose:** Phiên bản v2+
- **Tài nguyên tối thiểu:** 1 vCPU, 1 GB RAM, 10 GB SSD

---

## 2. Tải mã nguồn & Cấu hình môi trường

```bash
# Clone kho mã nguồn
git clone https://github.com/phattvh/OLP---RentCalc.git
cd OLP---RentCalc

# Tạo file cấu hình môi trường production
cp .env.example .env
```

Chỉnh sửa nội dung file `.env` phù hợp với thông số bảo mật production:
```ini
POSTGRES_DB=rentcalc
POSTGRES_USER=rentcalc_admin
POSTGRES_PASSWORD=MatKhauBaoMatChongDoan123!
DATABASE_URL=postgresql+psycopg://rentcalc_admin:MatKhauBaoMatChongDoan123!@db:5432/rentcalc
SECRET_KEY=ChuoiBiMatBaoMatChongDoanNgauNhien123!@#
ENV=production
```

---

## 3. Khởi chạy hệ thống bằng Docker Compose

```bash
# Khởi chạy toàn bộ dịch vụ (PostgreSQL + Web FastAPI) ở chế độ ngầm
docker compose -f docker-compose.prod.yml up -d --build

# Theo dõi tiến trình khởi động và migration database
docker compose -f docker-compose.prod.yml logs -f web
```

---

## 4. Cấu hình Nginx Reverse Proxy (Tùy chọn cho Domain & SSL)

Sao chép file `nginx.conf` vào cấu hình Nginx của hệ thống:
```bash
sudo cp nginx.conf /etc/nginx/sites-available/rentcalc
sudo ln -s /etc/nginx/sites-available/rentcalc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Cài đặt SSL Let's Encrypt tự động:
```bash
sudo certbot --nginx -d rentcalc.example.com
```

---

## 5. Kiểm tra tình trạng hoạt động (Health Check)

Kiểm tra endpoint `/health`:
```bash
curl -i http://localhost:8000/health
```

Kết quả mong đợi:
```json
HTTP/1.1 200 OK
content-type: application/json

{"status":"ok","version":"1.0.0"}
```

---

## 6. Sao lưu và Khôi phục dữ liệu (Backup & Restore)

```bash
# Sao lưu cơ sở dữ liệu PostgreSQL (chạy trực tiếp qua docker compose)
docker compose -f docker-compose.prod.yml exec -T db pg_dump -U rentcalc_admin rentcalc > backup_$(date +%Y%m%d).sql

# Khôi phục cơ sở dữ liệu
cat backup_20260909.sql | docker compose -f docker-compose.prod.yml exec -T db psql -U rentcalc_admin -d rentcalc
```
