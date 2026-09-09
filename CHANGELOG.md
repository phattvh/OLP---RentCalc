# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.0.0/), phiên bản theo [Semantic Versioning](https://semver.org/lang/vi/).

## [0.3.0] - 2026-09-09

### Added

- **Chia sẻ hóa đơn công khai (`/share/{token}`):** Cho phép người thuê phòng tra cứu trực tiếp bảng bóc tách tiền điện nước và tổng tiền phải trả mà không cần tạo tài khoản hoặc đăng nhập.
- **Xuất hóa đơn PDF chuẩn in ấn:** Tích hợp dịch vụ xuất file PDF chính thức hỗ trợ 100% Unicode tiếng Việt có dấu, căn lề chuẩn xác, có khu vực chữ ký xác nhận của hai bên.
- **Xác thực & Phân quyền (Role-Based Access):** Phân định hai vai trò Chủ nhà (`owner`) và Khách thuê (`tenant`) thông qua Cookie xác thực an toàn; người thuê tự động điều hướng về trang hóa đơn cá nhân (`/my-invoices`).
- **Cảnh báo công tơ quay vòng (Rollover Warning):** Hiển thị cảnh báo trực quan trên form nhập số công tơ khi chỉ số mới nhỏ hơn chỉ số cũ, tự động kích hoạt thuật toán bù quay vòng.
- **Bảng điều khiển quản trị (Dashboard):** 4 thẻ thống kê tổng quan (cơ sở, phòng, hóa đơn, cảnh báo thu vượt) và banner cảnh báo chế tài xử phạt theo Điều 31 Nghị định 133/2026/NĐ-CP.
- **Xác thực biểu mẫu Client-side & Tối ưu Mobile:** Kiểm tra logic nhập liệu ngay trên trình duyệt, giao diện co giãn mượt mà trên mọi độ phân giải.
- **Dữ liệu tài khoản Demo:** Bổ sung tài khoản mẫu `owner` (`owner123`) và `tenant101` (`tenant123`) trong `scripts/seed.py`.

### Changed

- **Cải tiến giao diện người dùng:**
  - Nút "Quay lại" được thiết kế dạng button nổi bật, dễ thao tác trên mọi trang chi tiết và biểu mẫu.
  - Thanh điều hướng (Navbar) đẩy menu sang sát lề phải, logo chữ `RentCalc` phẳng hiện đại.
  - Footer thiết kế 2 cột cân xứng (Thông tin hệ thống & Liên kết nhanh bên trái, Căn cứ pháp lý bên phải), dòng bản quyền MIT độc lập sát mép dưới.
  - Bảng biểu hóa đơn PDF được căn giữa theo chiều dọc (`valign=middle`) cho toàn bộ các ô dữ liệu và tiêu đề cột.

### Tests

- Bổ sung kiểm thử tự động cho module chia sẻ token, xuất PDF, phân quyền xác thực và kịch bản rollover: **49/49 tests pass 100%**, Code Coverage đạt **85%**.

---

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

---

## [0.1.0] - 2026-09-07

### Added

- Khởi tạo dự án, giấy phép MIT, tài liệu khung PoF.
- Core calculation engine: điện bậc thang có định mức, áp bậc 3 khi không kê khai, nước hai phương thức, đối chiếu thực thu.
- Bộ kiểm thử: 7 ca chính thức + edge cases (33 tests passed 100%, độ bao phủ code 96%).
