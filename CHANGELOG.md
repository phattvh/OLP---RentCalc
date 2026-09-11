# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.0.0/), phiên bản theo [Semantic Versioning](https://semver.org/lang/vi/).

## [1.0.0] - 2026-09-09

### Added

- **Hoàn thiện khả năng tiếp cận (Accessibility - a11y):** Tích hợp đầy đủ các thuộc tính WCAG/ARIA (`aria-label`, `aria-live="polite"`, `role="alert"`), nút skip-link "Bỏ qua menu điều hướng" cho người dùng bàn phím hoặc đọc màn hình.
- **Trang báo lỗi giao diện tùy biến (Custom Error Pages):** Bổ sung trang lỗi 404 ("Không tìm thấy trang") và 500 ("Lỗi máy chủ nội bộ") đồng bộ với nhận diện thương hiệu RentCalc.
- **Cấu hình triển khai Production hoàn chỉnh:** Cung cấp `docker-compose.prod.yml`, cấu hình Nginx Reverse Proxy (`nginx.conf`), và tài liệu hướng dẫn vận hành chi tiết tại `docs/DEPLOY.md`.
- **Trạng thái xác thực động trên Navbar:** Hiển thị danh tính người dùng đăng nhập (`Chủ trọ` / `Khách`), liên kết truy cập nhanh "Hóa đơn của tôi" cho người thuê, và nút "Đăng xuất" an toàn.
- **Endpoint kiểm tra sức khỏe hệ thống:** Route `/health` chuẩn hóa phục vụ giám sát container Docker và pipeline CI/CD.
- **Bảo mật xác thực & Bất biến hóa đơn:** Ký cookie bằng HMAC-SHA256 với secret nạp từ môi trường, bảo toàn nguyên vẹn snapshot và biểu giá hóa đơn lịch sử (immutability).
- **Khả năng cấu hình toàn diện & Biểu giá động N-bậc:** Cho phép tùy biến số lượng bậc điện linh hoạt (3, 5, 6, N bậc - thêm/xóa bậc trực quan), cấu hình ngưỡng định mức từng bậc cơ sở (kWh) và giới hạn quay vòng công tơ (max meter) trực tiếp từ giao diện quản trị.
- **Xác thực dữ liệu cấu hình biểu giá nghiêm ngặt (Config Payload Validation):** Chặn lưu các cấu hình không hợp lệ ngay từ tầng Web/Service (kiểm tra đơn giá không âm, thuế VAT [0, 1], phí BVMT [0, 1], định mức người > 0, fallback tier hợp lệ, bậc vô hạn duy nhất ở cuối).
- **Chuẩn hóa liên kết chia sẻ hóa đơn công khai:** Cập nhật nút sao chép link trên trang chi tiết hóa đơn trỏ chính xác đến route tra cứu `/share/{token}` với đầy đủ origin và giao diện trực quan.

### Changed

- **Tối ưu hóa hiệu năng tải trang:** Minify toàn diện file CSS tĩnh của Tailwind phục vụ môi trường production.
- **Nâng cấp nhận diện thương hiệu:** Cập nhật nhãn phiên bản `v1.0.0` trên toàn bộ Header, Footer, metadata ứng dụng và tài liệu kỹ thuật.
- **Tăng cường trải nghiệm điều hướng:** Tự động chuyển hướng người dùng theo vai trò khi truy cập trang đăng nhập.

### Tests

- Bổ sung kiểm thử tự động cho router `/health`, trang lỗi 404, trạng thái xác thực Navbar, bảo mật signed cookie HMAC, phân quyền RBAC, tính bất biến hóa đơn lịch sử, tạo biểu giá động 5 bậc, kiểm tra chặn lưu biểu giá lỗi (HTTP 400), sao chép link tra cứu công khai: **60/60 tests pass 100%**, Code Coverage đạt **85%**.
- Hoàn thành diễn tập chạy thử (dry-run) toàn bộ 7 ca kiểm thử chính thức của đề thi mà không có bất kỳ sai số nào.

---

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
