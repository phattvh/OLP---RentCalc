# Bộ quy tắc tính toán điện nước cho nhà cho thuê

> Trạng thái: SPEC. Đây là nguồn sự thật duy nhất cho app/core và tests.
> Mọi thay đổi quy tắc phải sửa tài liệu này TRƯỚC, rồi mới sửa test, cuối cùng sửa code.

## 1. Phạm vi

Mô tả bộ quy tắc đã cài đặt trong app/core, dùng làm căn cứ sinh test,
nghiệm thu và đối chiếu khi quy định pháp luật thay đổi.

## 2. Căn cứ pháp lý

| Văn bản                  | Ngày ban hành | Hiệu lực           | Nội dung dùng trong phần mềm                            |
| ------------------------ | ------------- | ------------------ | ------------------------------------------------------- |
| Quyết định 1279/QĐ-BCT   | 09/5/2025     | 10/5/2025          | Biểu giá điện sinh hoạt 6 bậc                           |
| Thông tư 60/2025/TT-BCT  | 2025          | 02/12/2025         | Định mức theo số người thuê; áp bậc 3 khi không kê khai |
| Nghị quyết 204/2025/QH15 | 2025          | đến hết 31/12/2026 | VAT điện sinh hoạt 8%                                   |
| Nghị định 133/2026/NĐ-CP | 2026          | 25/5/2026          | Khoản 7 & 11 Điều 13: Xử phạt 20–30 triệu thu tiền điện vượt, kèm hoàn trả |

## 3. Nguyên tắc cấu hình

Cấm viết cứng trong engine. Phải cấu hình được: bảng bậc điện (số bậc,
ngưỡng gốc, đơn giá), VAT điện, people_per_quota, bậc fallback khi không
kê khai, giá nước 2 phương thức, VAT nước, phí bảo vệ môi trường,
số đo tối đa công tơ.

## 4. Quy tắc điện

### 4.1 Biểu giá mặc định kỳ thi (cho 1 định mức)

| Bậc | Sản lượng trong bậc                 | Đơn giá đồng/kWh (chuỗi trong code) |
| --- | ----------------------------------- | ----------------------------------- |
| 1   | 50 đầu tiên                         | "1984"                              |
| 2   | 50 tiếp theo                        | "2050"                              |
| 3   | 100 tiếp theo                       | "2380"                              |
| 4   | 100 tiếp theo                       | "2998"                              |
| 5   | 100 tiếp theo                       | "3350"                              |
| 6   | phần còn lại (base_quantity = null) | "3460"                              |

### 4.2 Cách cộng dồn

Tiền trước thuế = Σ (sản lượng thuộc bậc i × đơn giá i), duyệt bậc 1 → 6.
LỖI SAI PHỔ BIẾN: lấy tổng sản lượng × đơn giá bậc chứa tổng đó.
Ví dụ sai: 120 kWh × 2.380 = 285.600.

### 4.3 Định mức

Q = số người / 4. Không làm tròn Q.
1 người = 0,25 | 2 = 0,50 | 3 = 0,75 | 4 = 1,00 | 5 = 1,25 …
Ngưỡng bậc i = ngưỡng gốc i × Q. Ngưỡng có thể thập phân, KHÔNG làm tròn.
Ví dụ Q = 1,25: bậc 1 = 62,5 kWh; bậc 2 = 62,5 kWh; bậc 3 = 125 kWh.

### 4.4 Không kê khai đầy đủ số người

Toàn bộ sản lượng × đơn giá bậc fallback (mặc định bậc 3 = 2380), cộng VAT.
Căn cứ: Thông tư 60/2025/TT-BCT (hợp đồng < 12 tháng và không kê khai).

### 4.5 VAT điện

vat = tiền trước thuế × vat_rate (mặc định "0.08", cấu hình được).

## 5. Quy tắc công tơ

Sản lượng = cuối kỳ − đầu kỳ (nếu cuối ≥ đầu).
Công tơ quay vòng (cuối < đầu): sản lượng = (max + 1) − đầu + cuối.
Công tơ 5 chữ số: max = 99.999 (cấu hình được).
Chuỗi hiển thị được chuẩn hóa: "00.120" → 120; "99.850" → 99850.
Chỉ số âm hoặc chuỗi sai định dạng → lỗi đầu vào.

## 6. Quy tắc nước

Phương thức volume: tiền trước thuế = m³ × đơn giá m³ (mặc định "8500").
Phương thức per_person: tiền trước thuế = số người × đơn giá người/tháng (mặc định "80000").
VAT nước = tiền trước thuế × "0.05".
Phí bảo vệ môi trường = tiền trước thuế × "0.10".
Cả hai tính trên tiền trước thuế; không tính phí trên phí.

## 7. Quy tắc làm tròn

Mọi phép trung gian giữ nguyên độ chính xác thập phân.
Chỉ làm tròn KẾT QUẢ CUỐI CỦA MỖI HÓA ĐƠN, đến đồng, nửa lên (HALF_UP).
Ví dụ: 151.097,4 → 151.097 | 701.524,8 → 701.525 | x,5 → lên.

## 8. Đối chiếu thực thu

chênh lệch = số thực thu − tổng tiền theo quy định.
Dương: người thuê trả thừa. Bằng 0: khớp. Âm: thu thấp hơn quy định.

## 9. Bảng nghiệm thu chính thức

| Mã    | Đầu vào                   | Breakdown (sản lượng × đơn giá)        | Trước thuế | Thuế                  | Kết quả                     |
| ----- | ------------------------- | -------------------------------------- | ---------- | --------------------- | --------------------------- |
| TC-01 | 4 người, 120 kWh          | 50×1984; 50×2050; 20×2380              | 249300     | 19944                 | 269244                      |
| TC-02 | 5 người, 200 kWh          | 62,5×1984; 62,5×2050; 75×2380          | 430625     | 34450                 | 465075                      |
| TC-03 | 1 người, 60 kWh           | 12,5×1984; 12,5×2050; 25×2380; 10×2998 | 139905     | 11192,4               | exact 151097,4 → 151097     |
| TC-04 | 99.850→00.120, 4 người    | 50×1984; 50×2050; 100×2380; 70×2998    | 649560     | 51964,8               | exact 701524,8 → 701525     |
| TC-05 | không kê khai, 120 kWh    | 120×2380 (phẳng bậc 3)                 | 285600     | 22848                 | 308448 (chênh TC-01: 39204) |
| TC-06 | nước 12 m³                | 12×8500                                | 102000     | VAT 5100 + BVMT 10200 | 117300                      |
| TC-07 | thực thu 480000 vs 269244 | —                                      | —          | —                     | chênh 210756, trả thừa      |

## 10. Chính sách biên và lỗi

- Q = 0: hợp lệ về toán học (mọi sản lượng rơi bậc cuối); kiểm tra nghiệp vụ
  nằm ở service tầng trên, không nằm trong engine.
- Config thiếu bậc vô hạn / thiếu bậc fallback / đơn giá âm / thuế suất âm
  → ném ConfigError.
- Chỉ số công tơ âm, chuỗi sai định dạng, thiếu tham số theo phương thức
  → ném lỗi đầu vào.

## 11. Ánh xạ kiểm thử

| Mục spec   | File test                                                       |
| ---------- | --------------------------------------------------------------- |
| §4, §9     | tests/official/test_official_cases.py                           |
| §5         | tests/core/test_meter.py                                        |
| §4.3       | tests/core/test_quota.py                                        |
| §4.2, §4.4 | tests/core/test_electricity_tiered.py, test_electricity_flat.py |
| §6         | tests/core/test_water.py                                        |
| §7         | tests/core/test_rounding.py                                     |
| §8         | tests/core/test_comparison.py                                   |
| §10        | tests/core/test_month.py                                        |
