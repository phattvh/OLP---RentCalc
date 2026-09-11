# Thư viện bên thứ ba và giấy phép nguồn mở (Third-Party Licenses)

## Dự án RentCalc cam kết sử dụng 100% phần mềm và thư viện nguồn mở có giấy phép tương thích với MIT License.

## 1. Đang sử dụng trong Task 01 (Kiểm thử & Lõi thuật toán)

| Thư viện       | Phiên bản | Giấy phép (License) | Mục đích sử dụng                                |
| -------------- | --------- | ------------------- | ----------------------------------------------- |
| **pytest**     | `>=8.3`   | MIT License         | Khung kiểm thử tự động (Test Runner)            |
| **pytest-cov** | `>=5.0`   | MIT License         | Đo độ bao phủ mã nguồn kiểm thử (Code Coverage) |

---

## 2. Thư viện lõi hệ thống & Ứng dụng Web (Core & Web Layer)

Tất cả các thư viện dưới đây đã được tích hợp và hoạt động chính thức trong bản phát hành RentCalc `v1.0.0`:
| Thư viện | Giấy phép (License) | Mục đích sử dụng |
|---|---|---|
| **fastapi** | MIT License | Web Framework API, Routing và Dependency Injection |
| **uvicorn** | BSD 3-Clause | ASGI Web Server hiệu năng cao |
| **sqlalchemy** | MIT License | Object Relational Mapper (ORM) và quản lý kết nối CSDL |
| **alembic** | MIT License | Quản lý phiên bản Database Schema Migrations |
| **psycopg** | LGPL / BSD | Driver kết nối chuẩn hóa cơ sở dữ liệu PostgreSQL 16 |
| **pydantic** | MIT License | Xác thực dữ liệu và Data Modeling chặt chẽ |
| **pydantic-settings** | MIT License | Nạp cấu hình ứng dụng từ biến môi trường (.env) |
| **jinja2** | BSD 3-Clause | Template Engine render giao diện người dùng Server-Side |
| **httpx** | BSD 3-Clause | HTTP Client phục vụ kiểm thử tích hợp Web API |
| **python-multipart** | Apache License 2.0 | Xử lý dữ liệu biểu mẫu Form POST đăng nhập & cấu hình |
| **xhtml2pdf** | Apache License 2.0 | Xuất hóa đơn chuẩn in ấn định dạng PDF tiếng Việt Unicode |

---

## 3. Lệnh kiểm tra giấy phép tự động

Để trích xuất toàn bộ danh mục giấy phép kể cả các thư viện phụ thuộc bắc cầu (transitive dependencies):

```bash
pip install pip-licenses && pip-licenses --format=markdown
```
