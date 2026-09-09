# Thư viện bên thứ ba và giấy phép nguồn mở (Third-Party Licenses)

## Dự án RentCalc cam kết sử dụng 100% phần mềm và thư viện nguồn mở có giấy phép tương thích với MIT License.

## 1. Đang sử dụng trong Task 01 (Kiểm thử & Lõi thuật toán)

| Thư viện       | Phiên bản | Giấy phép (License) | Mục đích sử dụng                                |
| -------------- | --------- | ------------------- | ----------------------------------------------- |
| **pytest**     | `>=8.3`   | MIT License         | Khung kiểm thử tự động (Test Runner)            |
| **pytest-cov** | `>=5.0`   | MIT License         | Đo độ bao phủ mã nguồn kiểm thử (Code Coverage) |

---

## 2. Dự kiến tích hợp từ Task 02 (Web & Database)

Tất cả các thư viện dưới đây đã được rà soát giấy phép trước khi đưa vào kiến trúc:
| Thư viện | Giấy phép (License) | Mục đích sử dụng |
|---|---|---|
| **fastapi** | MIT License | Web Framework API & Routing |
| **uvicorn** | BSD 3-Clause | ASGI Web Server |
| **sqlalchemy** | MIT License | Object Relational Mapper (ORM) |
| **alembic** | MIT License | Quản lý phiên bản Database Migrations |
| **psycopg** | LGPL / BSD | Driver kết nối cơ sở dữ liệu PostgreSQL |
| **pydantic** | MIT License | Xác thực dữ liệu và Schema Data Modeling |
| **pydantic-settings** | MIT License | Nạp cấu hình ứng dụng và biến môi trường |
| **jinja2** | BSD 3-Clause | Template Engine render giao diện HTML |
| **httpx** | BSD 3-Clause | HTTP Client phục vụ kiểm thử tích hợp |
| **python-multipart** | Apache License 2.0 | Xử lý dữ liệu Form POST đăng nhập & cấu hình |
| **xhtml2pdf** | Apache License 2.0 | Xuất hóa đơn chuẩn định dạng PDF tiếng Việt Unicode |

---

## 3. Lệnh kiểm tra giấy phép tự động

Để trích xuất toàn bộ danh mục giấy phép kể cả các thư viện phụ thuộc bắc cầu (transitive dependencies):

```bash
pip install pip-licenses && pip-licenses --format=markdown
```
