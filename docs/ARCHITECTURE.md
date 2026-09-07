# Kiến Trúc Hệ Thống RentCalc

> Trạng thái: **VERIFIED v0.2** (Khớp 100% với cài đặt `app/core` và 32/32 tests passed).

---

## 1. Mô Hình Phân Tầng (Layered Architecture)

Hệ thống RentCalc được thiết kế theo mô hình **Modular Monolith** kết hợp nguyên lý **Clean Architecture**, đảm bảo phân tách trách nhiệm rõ ràng giữa các tầng:

```mermaid
flowchart TB
    subgraph Presentation ["1. Presentation Layer"]
        A["Jinja2 Templates + HTMX + Tailwind CSS"]
    end
    subgraph Web ["2. Web Layer"]
        B["FastAPI Routers / Forms"]
    end
    subgraph Application ["3. Application Services"]
        C["CalculationService / ConfigService / InvoiceService"]
    end
    subgraph Core ["4. Core Calculation Engine (Pure Python)"]
        D["Thuật toán tính toán điện nước<br/>Pure Python + decimal.Decimal"]
    end
    subgraph Infrastructure ["5. Infrastructure Layer"]
        E[("PostgreSQL + SQLAlchemy + Alembic")]
    end

    A --> B
    B --> C
    C --> D
    C --> E
```

### Nguyên tắc phân tầng bắt buộc:

- **Tầng Core độc lập 100%**: Không phụ thuộc vào web framework, database, biến môi trường hay file hệ thống.
- **Quy tắc cấm import ngược**: Tầng `app/core` TUYỆT ĐỐI KHÔNG import từ `fastapi`, `sqlalchemy`, `alembic`, `app.db`, `app.web`.
- **Dòng dữ liệu đơn chiều**: Yêu cầu đi từ Presentation -> Web -> Service -> Core / Infrastructure.

---

## 2. Đặc Tả Thuật Toán Tính Điện Bậc Thang (Tiered Algorithm)

Sơ đồ dưới đây mô tả chính xác vòng lặp phân bổ sản lượng điện theo định mức Q và cộng dồn lũy tiến 6 bậc:

```mermaid
flowchart TD
    A["Đầu vào: consumption, people_count, config"] --> B["Tính định mức: quota = people_count / people_per_quota"]
    B --> C["Khởi tạo: remaining = consumption, subtotal = 0, breakdown = []"]
    C --> D{"Còn bậc chưa duyệt trong danh sách?"}
    D -- Có --> E{"base_quantity == null?<br/>(Bậc vô hạn cuối cùng)"}
    E -- Có --> F["tier_qty = remaining"]
    E -- Không --> G["Hạn mức bậc: tier_limit = base_quantity × quota"]
    G --> H["Sản lượng bậc: tier_qty = min(remaining, tier_limit)"]
    F --> I["Thành tiền bậc: amount = tier_qty × unit_price"]
    H --> I
    I --> J["Cộng dồn: subtotal += amount<br/>remaining -= tier_qty<br/>Ghi nhận dòng breakdown"]
    J --> D
    D -- Hết bậc --> K{"remaining > 0?"}
    K -- Còn thừa --> L["Ném lỗi ConfigError (thiếu bậc vô hạn)"]
    K -- Không --> M["Tính thuế: vat = subtotal × vat_rate"]
    M --> N["Tổng chính xác: total_exact = subtotal + vat"]
    N --> O["Làm tròn cuối cùng: total_rounded = round_vnd(total_exact)"]
```

---

## 3. Cấu Trúc Thư Mục `app/core`

```txt
app/core/
├── __init__.py          # Package initialization
├── errors.py            # Hệ thống ngoại lệ phân cấp (RentCalcError, ConfigError, InputError...)
├── types.py             # Cấu trúc dữ liệu bất biến (frozen dataclasses, Decimal)
├── decimal_utils.py     # Tiện ích số học chính xác cao (prec=50, round_vnd HALF_UP)
├── meter.py             # Xử lý chỉ số và quay vòng công tơ cơ khí
├── quota.py             # Tính định mức số hộ Q (không làm tròn)
├── electricity.py       # Tính điện bậc thang lũy tiến và đồng giá không kê khai
├── water.py             # Tính tiền nước (theo khối hoặc theo đầu người)
└── comparison.py        # Đối chiếu số tiền thực thu và cảnh báo thu vượt
```
