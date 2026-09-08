# Changelog

Định dạng theo Keep a Changelog, phiên bản theo Semantic Versioning.

## [0.2.0] - 2026-09-08

### Added

- Tầng cơ sở dữ liệu: 5 bảng thực thể (Property, Room, MeterReading, TariffConfig, Invoice) trên PostgreSQL 16.
- Quản lý di chuyển lược đồ tự động bằng Alembic (initial schema).
- Tầng Repositories và Application Services điều phối nghiệp vụ tích hợp Core Engine.
- Tầng Web FastAPI: 13 routes xử lý CRUD cơ sở, phòng trọ, ghi chỉ số công tơ, sinh hóa đơn.
- Giao diện Jinja2 Templates kết hợp Tailwind CSS biên dịch độc lập và HTMX.
- Trang chi tiết hóa đơn bóc tách minh bạch từng bậc thang lũy tiến và form đối chiếu thực thu theo Nghị định 133/2026/NĐ-CP.
- Script nạp dữ liệu demo ban đầu (scripts/seed.py).
- Tài liệu hướng dẫn cài đặt từ mã nguồn sạch (docs/INSTALL.md) và kịch bản demo (docs/DEMO.md).

## [0.1.0] - 2026-09-07

### Added

- Khởi tạo dự án, giấy phép MIT, tài liệu khung PoF.
- Core calculation engine: điện bậc thang có định mức, áp bậc 3 khi không kê khai, nước hai phương thức, đối chiếu thực thu.
- Bộ kiểm thử: 7 ca chính thức + edge cases (33 tests passed 100%, độ bao phủ code 96%).
