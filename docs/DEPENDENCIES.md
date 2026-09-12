# Danh mục thư viện phụ thuộc và giấy phép nguồn mở (Dependencies & Licenses)

> **Dự án:** RentCalc (v1.0.0)  
> **Giấy phép chính:** MIT License  
> **Cam kết bản quyền PMNM:** Toàn bộ các thư viện bên thứ ba được sử dụng trong dự án đều là mã nguồn mở với giấy phép tương thích hoàn toàn (Permissive Licenses: MIT, BSD, Apache 2.0, LGPL-3.0) với giấy phép MIT của dự án.

---

## 1. Thư viện ứng dụng Web & Cơ sở dữ liệu (Runtime / Production)

Các thư viện nền tảng phục vụ vận hành hệ thống máy chủ FastAPI, xử lý ORM, xác thực dữ liệu, template engine và xuất hóa đơn PDF:

| Thư viện | Phiên bản yêu cầu | Giấy phép (License) | Mục đích sử dụng trong hệ thống |
| :--- | :--- | :--- | :--- |
| **fastapi** | `>=0.115,<1.0` | MIT License | Khung ứng dụng Web hiệu năng cao, định tuyến (Routing) và Dependency Injection cho RBAC. |
| **uvicorn** | `>=0.30,<1.0` | BSD 3-Clause | Máy chủ ASGI Web Server đa luồng phục vụ ứng dụng FastAPI. |
| **sqlalchemy** | `>=2.0,<3.0` | MIT License | Object Relational Mapper (ORM 2.0) quản lý truy vấn và kết nối cơ sở dữ liệu PostgreSQL. |
| **alembic** | `>=1.13,<2.0` | MIT License | Công cụ quản lý lịch sử và thực thi Database Schema Migrations. |
| **psycopg** | `>=3.2,<4.0` | LGPL-3.0 | Driver kết nối chuẩn hóa (DB-API) tương tác trực tiếp với cơ sở dữ liệu PostgreSQL 16. |
| **pydantic** | `>=2.8,<3.0` | MIT License | Định kiểu (Data Modeling), kiểm tra và xác thực dữ liệu đầu vào chặt chẽ. |
| **pydantic-settings** | `>=2.4,<3.0` | MIT License | Nạp và xác thực cấu hình hệ thống từ biến môi trường (`.env`). |
| **jinja2** | `>=3.1,<4.0` | BSD 3-Clause | Template Engine render giao diện HTML Server-Side và mẫu hóa đơn in ấn. |
| **python-multipart** | `>=0.0.9` | Apache-2.0 | Bộ phân giải dữ liệu biểu mẫu HTTP POST (`multipart/form-data` và form URL-encoded). |
| **xhtml2pdf** | `>=0.2.16` | Apache-2.0 | Bộ chuyển đổi HTML/CSS sang file PDF chuẩn in ấn, hỗ trợ Unicode tiếng Việt đầy đủ. |

---

## 2. Thư viện phát triển & Kiểm thử tự động (Development & Testing)

Các công cụ phục vụ kiểm thử đơn vị, kiểm thử tích hợp và kiểm soát chất lượng mã nguồn:

| Thư viện | Phiên bản yêu cầu | Giấy phép (License) | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| **pytest** | `>=8.3` | MIT License | Khung thực thi kiểm thử tự động (Test Runner) cho toàn bộ 63 ca kiểm thử. |
| **pytest-cov** | `>=5.0` | MIT License | Công cụ đo lường và lập báo cáo độ bao phủ mã nguồn (Code Coverage $\ge$ 85%). |
| **httpx** | `>=0.27` | BSD 3-Clause | HTTP Client bất đồng bộ phục vụ giả lập request kiểm thử tích hợp qua `TestClient`. |

---

## 3. Ma trận tương thích giấy phép mã nguồn mở (License Compatibility)

Hệ thống tuân thủ nghiêm ngặt các quy định về sở hữu trí tuệ và quyền tác giả phần mềm nguồn mở:

| Loại giấy phép | Thư viện áp dụng | Tính tương thích với Giấy phép MIT của RentCalc |
| :--- | :--- | :--- |
| **MIT License** | `fastapi`, `sqlalchemy`, `alembic`, `pydantic`, `pydantic-settings`, `pytest`, `pytest-cov` | **Tương thích hoàn toàn:** Cho phép sao chép, sửa đổi, hợp nhất và phân phối tự do. |
| **BSD 3-Clause** | `uvicorn`, `jinja2`, `httpx` | **Tương thích hoàn toàn:** Yêu cầu giữ nguyên thông tin bản quyền và từ chối bảo đảm. |
| **Apache 2.0** | `python-multipart`, `xhtml2pdf` | **Tương thích hoàn toàn:** Cấp quyền sử dụng bằng sáng chế và bản quyền, phù hợp tích hợp vào dự án MIT. |
| **LGPL-3.0** | `psycopg` (driver binary) | **Tương thích:** Sử dụng dưới dạng thư viện độc lập liên kết động (Dynamic Linking / Standard Python package), không làm ảnh hưởng đến tính chất giấy phép MIT của toàn bộ mã nguồn ứng dụng. |

---

## 4. Quy trình kiểm tra bản quyền tự động (Audit Commands)

Để trích xuất danh sách giấy phép của toàn bộ các gói thư viện (bao gồm cả các thư viện phụ thuộc bắc cầu - transitive dependencies):

```bash
# 1. Cài đặt công cụ kiểm tra giấy phép
pip install pip-licenses

# 2. Xuất báo cáo giấy phép theo định dạng Markdown
pip-licenses --format=markdown --output-file=licenses_report.md

# 3. Liệt kê các thư viện kèm đường dẫn giấy phép chi tiết
pip-licenses --with-urls
```
