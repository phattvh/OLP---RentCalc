# RentCalc - Minh Bạch Hóa Chi Phí Dịch Vụ Thiết Yếu Nhà Trọ

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Tests](https://img.shields.io/badge/tests-51%2F51%20passed-success.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

- **Tác giả:** Phat Tran Vu Hoa
- **Dự thi:** Olympic Tin học Sinh viên 2026 — Khối Phần mềm nguồn mở (PMNM)
- **Giấy phép:** MIT License.

---

## Giới thiệu

**RentCalc** là ứng dụng web mã nguồn mở giúp minh bạch hóa chi phí điện và nước sinh hoạt tại các khu nhà trọ, bảo vệ quyền lợi hợp pháp của sinh viên và người thuê trọ theo chuẩn quy chuẩn pháp luật Việt Nam.

### Căn cứ pháp lý áp dụng:

- **Quyết định 2741/QĐ-BCT & QĐ 1279/QĐ-BCT:** Biểu giá bán lẻ điện sinh hoạt 6 bậc thang lũy tiến.
- **Thông tư 60/2025/TT-BCT:** Cơ chế tính định mức sử dụng điện cho người thuê trọ (4 người = 1 định mức hộ gia đình) và áp giá Bậc 3 khi chưa kê khai tạm trú.
- **Nghị định 133/2026/NĐ-CP (Điều 31):** Chế tài xử phạt vi phạm hành chính từ 20.000.000 đ đến 30.000.000 đ khi chủ trọ thu tiền điện nước cao hơn quy định.

---

## Trạng thái phát triển các giai đoạn

- ✅ **Task 01: Core Calculation Engine (`v0.1.0`)** — Hoàn thành (33/33 tests pass, 96% coverage).
- ✅ **Task 02: Database + Web Layer + CRUD (`v0.2.0`)** — Hoàn thành (PostgreSQL, FastAPI, CRUD, Snapshot).
- ✅ **Task 03: Advanced Features + UI Polish + Public Page (`v0.3.0`)** — Hoàn thành (Public share, Unicode PDF, RBAC Auth, Rollover warning, Dashboard alert).
- ✅ **Task 04: Final Polish + Presentation + Production Release (`v1.0.0`)** — Hoàn thành:
  - Khả năng tiếp cận: Chuẩn ARIA (`aria-label`, `role="alert"`), skip-link hỗ trợ đọc màn hình.
  - Tối ưu hiệu năng: Minify CSS Tailwind, endpoint kiểm tra sức khỏe `/health`.
  - Xử lý lỗi giao diện tùy biến: Trang 404 & 500, trạng thái xác thực động và nút Đăng xuất trên Navbar.
  - Sẵn sàng triển khai Production: `docker-compose.prod.yml`, `nginx.conf`, hướng dẫn [docs/DEPLOY.md](docs/DEPLOY.md).
  - Tài liệu bảo vệ đề tài: Bộ 15 slide [docs/PRESENTATION.md](docs/PRESENTATION.md) và kịch bản diễn tập 15 phút chi tiết từng giây [docs/REHEARSAL.md](docs/REHEARSAL.md).
  - Kiểm thử tự động: **51/51 tests pass (100%)**, Coverage **85%**.

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

## Tài liệu dự án & Trình diễn

- Hướng dẫn cài đặt sạch: [docs/INSTALL.md](docs/INSTALL.md)
- Hướng dẫn triển khai Production: [docs/DEPLOY.md](docs/DEPLOY.md)
- Kịch bản demo 7 trường hợp kiểm thử: [docs/DEMO.md](docs/DEMO.md)
- Bộ slide thuyết trình 15 phút: [docs/PRESENTATION.md](docs/PRESENTATION.md)
- Kịch bản diễn tập từng giây: [docs/REHEARSAL.md](docs/REHEARSAL.md)
- Lịch sử thay đổi các phiên bản: [CHANGELOG.md](CHANGELOG.md)
- Danh mục giấy phép thư viện bên thứ ba: [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md)

---

## Giấy phép

Mã nguồn được phát hành theo giấy phép mã nguồn mở **MIT** — xem chi tiết tại [LICENSE](LICENSE).
