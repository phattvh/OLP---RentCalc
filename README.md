# RentCalc - Minh Bạch Hóa Chi Phí Dịch Vụ Thiết Yếu Nhà Trọ

Tác giả: Phat Tran Vu Hoa
Giấy phép: MIT License.

---

## Giới thiệu

RentCalc là ứng dụng web mã nguồn mở giúp minh bạch hóa chi phí điện và nước sinh hoạt tại các khu nhà trọ, bảo vệ quyền lợi hợp pháp của sinh viên và người thuê trọ.

### Căn cứ pháp lý:

- Quyết định 1279/QĐ-BCT: Biểu giá bán lẻ điện sinh hoạt 6 bậc thang.
- Thông tư 60/2025/TT-BCT: Cơ chế tính định mức sử dụng điện và áp giá Bậc 3 khi không kê khai tạm trú.
- Nghị quyết 204/2025/QH15: Thuế suất VAT đối với điện sinh hoạt.
- Nghị định 133/2026/NĐ-CP: Xử phạt vi phạm hành chính 20–30 triệu đồng khi thu tiền điện nước cao hơn quy định.

---

## Trạng thái phát triển

- Task 01: Core Calculation Engine (v0.1.0) — Hoàn thành (33/33 tests pass, 96% coverage).
- Task 02: Database + Web Layer + CRUD (v0.2.0) — Hoàn thành:
  - Database: PostgreSQL 16 + SQLAlchemy 2.0 + Alembic migrations.
  - Web: FastAPI + Jinja2 Templates + Tailwind CSS compiled + HTMX.
  - Chức năng: CRUD cơ sở, phòng trọ, công tơ rollover, bóc tách hóa đơn lũy tiến, đối chiếu thực thu.

---

## Cài đặt nhanh

Xem hướng dẫn chi tiết tại docs/INSTALL.md:

```bash
docker compose up -d db
pip install -r requirements.txt
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Truy cập: http://localhost:8000

## Giấy phép

MIT — xem [LICENSE](LICENSE). Thư viện bên thứ ba: xem [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md).
