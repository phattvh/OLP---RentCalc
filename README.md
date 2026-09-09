# RentCalc - Minh Bạch Hóa Chi Phí Dịch Vụ Thiết Yếu Nhà Trọ

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Tests](https://img.shields.io/badge/tests-56%2F56%20passed-success.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

- **Tác giả:** Phat Tran Vu Hoa
- **Dự thi:** Olympic Tin học Sinh viên 2026 — Khối Phần mềm nguồn mở (PMNM)
- **Giấy phép:** MIT License.

---

## Giới thiệu

**RentCalc** là ứng dụng web mã nguồn mở giúp minh bạch hóa chi phí điện và nước sinh hoạt tại các khu nhà trọ, bảo vệ quyền lợi hợp pháp của sinh viên và người thuê trọ theo chuẩn quy chuẩn pháp luật Việt Nam.

### Quy tắc tính toán & Căn cứ pháp lý:

- **Quy tắc tính toán cuộc thi:** Triển khai chính xác theo các giá trị và quy tắc ấn định trong đề thi Olympic Tin học Sinh viên 2026 — Khối Phần mềm Nguồn mở (PMNM).
- **Căn cứ pháp lý áp dụng theo đề bài:**
  - **Quyết định 1279/QĐ-BCT:** Biểu giá bán lẻ điện sinh hoạt 6 bậc thang lũy tiến.
  - **Thông tư 60/2025/TT-BCT:** Cơ chế tính định mức sử dụng điện cho người thuê trọ (4 người = 1 định mức hộ gia đình) và áp giá Bậc 3 khi chưa kê khai tạm trú.
  - **Nghị định 133/2026/NĐ-CP (Điều 31):** Chế tài xử phạt vi phạm hành chính từ 20.000.000 đ đến 30.000.000 đ khi chủ trọ thu tiền điện nước cao hơn quy định.
- **Tính linh hoạt:** Toàn bộ biểu giá, ngưỡng bậc, thuế suất và quy tắc định mức được cấu hình trực quan từ giao diện quản trị, không viết cứng (hard-code) trong mã nguồn.

---

## Trạng thái phát triển các giai đoạn

- ✅ **Task 01: Core Calculation Engine (`v0.1.0`)** — Hoàn thành (33/33 tests pass, 96% coverage).
- ✅ **Task 02: Database + Web Layer + CRUD (`v0.2.0`)** — Hoàn thành (PostgreSQL, FastAPI, CRUD, Snapshot).
- ✅ **Task 03: Advanced Features + UI Polish + Public Page (`v0.3.0`)** — Hoàn thành (Public share, Unicode PDF, RBAC Auth, Rollover warning, Dashboard alert).
- ✅ **Task 04: Final Polish + Production Release (`v1.0.0`)** — Hoàn thành:
  - Khả năng tiếp cận: Chuẩn ARIA (`aria-label`, `role="alert"`), skip-link hỗ trợ đọc màn hình.
  - Tối ưu hiệu năng: Minify CSS Tailwind, endpoint kiểm tra sức khỏe `/health`.
  - Xử lý lỗi giao diện tùy biến: Trang 404 & 500, trạng thái xác thực động và nút Đăng xuất trên Navbar.
  - Sẵn sàng triển khai Production: `docker-compose.prod.yml`, `nginx.conf`, hướng dẫn [docs/DEPLOY.md](docs/DEPLOY.md).
  - Kiểm thử tự động: **56/56 tests pass (100%)**, Coverage **85%**.

---

## Cài đặt nhanh

Xem hướng dẫn chi tiết tại [docs/INSTALL.md](docs/INSTALL.md):

```bash
docker compose up -d db
pip install -r requirements.txt
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Truy cập: **http://localhost:8000**

- Tài khoản Chủ nhà: `owner` / `owner123`
- Tài khoản Khách thuê: `tenant101` / `tenant123`
- Trang chia sẻ công khai: `http://localhost:8000/share/demo-token-101`

---

## Tài liệu kỹ thuật dự án

- Hướng dẫn cài đặt sạch: [docs/INSTALL.md](docs/INSTALL.md)
- Hướng dẫn triển khai Production: [docs/DEPLOY.md](docs/DEPLOY.md)
- Kịch bản demo 7 trường hợp kiểm thử: [docs/DEMO.md](docs/DEMO.md)
- Lịch sử thay đổi các phiên bản: [CHANGELOG.md](CHANGELOG.md)
- Danh mục giấy phép thư viện bên thứ ba: [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md)

---

## Giấy phép

Mã nguồn được phát hành theo giấy phép mã nguồn mở **MIT** — xem chi tiết tại [LICENSE](LICENSE).
