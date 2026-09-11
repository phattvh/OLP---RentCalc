# Judge Demo Guide — Hướng Dẫn Trình Diễn Cho Ban Giám Khảo (v1.0.0)

> **Lưu ý:** Tài liệu này được thiết kế riêng cho phiên bảo vệ sản phẩm 15 phút tại **Olympic Tin học Sinh viên 2026 — Khối Phần mềm Nguồn mở (PMNM)**. Tài liệu hướng dẫn chi tiết từng bước thao tác thực tế trên giao diện để Ban Giám Khảo kiểm chứng tính đúng đắn của giải thuật, tính minh bạch pháp lý và kiến trúc mở.

---

## Chuẩn bị môi trường

1. Đảm bảo ứng dụng đang chạy tại: **http://localhost:8000**
2. Đã nạp dữ liệu mẫu bằng lệnh: `python scripts/seed.py`

---

## Kịch bản 1: Phòng đã kê khai tạm trú (Biểu giá bậc thang có định mức)

- **Đối tượng:** Phòng 101 (4 nhân khẩu $\rightarrow$ 1 định mức hộ gia đình theo Thông tư 60/2025/TT-BCT).

1. Truy cập: **http://localhost:8000/properties** $\rightarrow$ chọn **"Nhà trọ Mẫu TP.HCM"** $\rightarrow$ chọn **"Phòng 101"**.
2. Nhấn nút **"+ Nhập chỉ số công tơ"**:
   - Điện: Tháng `2026-09`, số cũ `0`, số mới `120` (Tiêu thụ 120 kWh).
   - Nước: Tháng `2026-09`, số cũ `0`, số mới `16` (Tiêu thụ 16 m³).
3. Quay lại trang phòng $\rightarrow$ tại mục **"Phát hành hóa đơn tính tiền"**, chọn kỳ `2026-09` $\rightarrow$ nhấn **"Tính tiền & Xuất hóa đơn"**.
4. **Kiểm tra kết quả bóc tách:**
   - Bậc 1 (50 kWh): 99.200 đ
   - Bậc 2 (50 kWh): 102.500 đ
   - Bậc 3 (20 kWh): 47.600 đ
   - Tiền điện trước thuế: 249.300 đ $\rightarrow$ Thuế GTGT 8%: 19.944 đ $\rightarrow$ Tổng tiền điện (làm tròn): **269.244 đ**.
   - Tiền nước (16 m³ có VAT 5% & Phí BVMT 10%): **156.400 đ**.
   - Tổng cộng số tiền theo quy định: **425.644 đ**.
5. **Đối chiếu thực thu:**
   - Nhập số tiền chủ nhà thu: `500000` $\rightarrow$ Nhấn **"Đối chiếu chênh lệch"**.
   - Hệ thống hiển thị khung đỏ cảnh báo: **Thu vượt +74.356 đ** kèm mức phạt vi phạm 20.000.000 đ – 30.000.000 đ theo **khoản 7 Điều 13 Nghị định 133/2026/NĐ-CP**!

---

## Kịch bản 2: Phòng không kê khai tạm trú (Áp đồng giá Bậc 3)

- **Đối tượng:** Phòng 102 (Không kê khai tạm trú).

1. Vào chi tiết **Phòng 102** $\rightarrow$ Nhập chỉ số điện tháng `2026-09`: số cũ `0`, số mới `100` (100 kWh).
2. Phát hành hóa đơn tháng `2026-09`.
3. **Kiểm chứng:** Toàn bộ 100 kWh bị áp đồng giá Bậc 3 (2.380 đ/kWh) không chia bậc $\rightarrow$ Tiền điện trước thuế: 238.000 đ $\rightarrow$ Sau thuế VAT 8%: **257.040 đ**.

---

## Kịch bản 3: Xuất hóa đơn định dạng PDF in ấn chuẩn tiếng Việt Unicode

1. Tại trang chi tiết hóa đơn, nhấn nút **"Xuất file PDF"** (hoặc truy cập `/invoices/{id}/pdf`).
2. Trình duyệt tải xuống file PDF: `hoa-don-2026-09-phong-1.pdf`.
3. **Kiểm chứng file PDF:**
   - Tiêu đề: *HỆ THỐNG QUẢN LÝ NHÀ TRỌ RENTCALC*.
   - Bảng biểu bóc tách sắc nét, hỗ trợ 100% tiếng Việt Unicode có dấu không bị vỡ font hay lỗi ô vuông.
   - Các cột số liệu và tiêu đề được căn giữa theo chiều dọc hoàn hảo.
   - Có đầy đủ khu vực chữ ký xác nhận của Người thuê phòng và Đại diện chủ cơ sở.

---

## Kịch bản 4: Chia sẻ hóa đơn công khai không cần đăng nhập (`/share/{token}`)

1. Tại trang chi tiết hóa đơn (với quyền chủ nhà), lấy mã chia sẻ tại mục **"Mã chia sẻ cho người thuê"** (ví dụ token: `abc123xyz...`).
2. Mở trình duyệt ẩn danh (Incognito) hoặc thiết bị di động (không cần đăng nhập tài khoản).
3. Truy cập đường dẫn: **http://localhost:8000/share/{token}**
4. **Kiểm chứng:**
   - Người thuê xem được bảng bóc tách chi tiết tiền điện, tiền nước và tổng số tiền phải thanh toán dưới dạng chỉ đọc (Read-only).
   - Người thuê có thể nhấn **"Tải hóa đơn PDF"** trực tiếp từ trang chia sẻ này mà không cần đăng nhập.
   - Nếu nhập token không hợp lệ (ví dụ: `/share/invalid_token`), hệ thống trả về mã lỗi HTTP 404 thân thiện.

---

## Kịch bản 5: Phân quyền tài khoản Chủ nhà (Owner) và Khách thuê (Tenant)

1. **Đăng nhập với vai trò Khách thuê:**
   - Truy cập **http://localhost:8000/login**, đăng nhập tài khoản: `tenant101` / `tenant123`.
   - Hệ thống tự động chuyển hướng tới: **http://localhost:8000/my-invoices**.
   - Khách thuê chỉ xem được các hóa đơn thuộc về **Phòng 101** của mình.
   - Nếu khách thuê cố tình truy cập các đường dẫn quản trị (như `/properties/new`, `/admin/configs`), hệ thống từ chối quyền truy cập (401 / 403) bảo vệ dữ liệu tuyệt đối.
2. **Đăng xuất và đăng nhập vai trò Chủ nhà:**
   - Nhấn **"Đăng xuất"** $\rightarrow$ Đăng nhập với: `owner` / `owner123`.
   - Chủ nhà có toàn quyền xem Dashboard, quản lý phòng, phát hành hóa đơn và chỉnh sửa biểu giá.

---

## Kịch bản 6: Cảnh báo chỉ số công tơ quay vòng (Rollover Warning)

1. Vào chi tiết **Phòng 101** $\rightarrow$ Chọn **"+ Nhập chỉ số công tơ"**.
2. Nhập kỳ tháng mới: `2026-10`.
3. Nhập số công tơ điện: Số cũ `9950`, Số mới `50` (Chỉ số mới nhỏ hơn chỉ số cũ do công tơ quay vòng qua mốc 10.000).
4. **Kiểm chứng:**
   - Giao diện lập tức kích hoạt banner cảnh báo màu vàng: *"Phát hiện chỉ số mới nhỏ hơn chỉ số cũ. Hệ thống tự động kích hoạt thuật toán bù quay vòng (Rollover Handling) theo mốc 10.000 kWh"*.
   - Sản lượng tiêu thụ tính toán chính xác: `(10.000 - 9.950) + 50 = 100 kWh`.

---

## Kịch bản 7: Bảng điều khiển Dashboard & Cảnh báo NĐ 133/2026/NĐ-CP

1. Truy cập trang chủ: **http://localhost:8000**
2. **Kiểm chứng Bảng điều khiển:**
   - 4 thẻ chỉ số thống kê (Cơ sở, Phòng đang quản lý, Hóa đơn phát hành, Cảnh báo thu vượt) hiển thị cân đối trên 1 hàng 4 cột.
   - Nếu có hóa đơn thu vượt mức trần nhà nước, banner cảnh báo vi phạm pháp lý màu đỏ hiển thị nổi bật với biểu tượng tam giác chấm than ⚠️, viện dẫn chính xác **khoản 7 Điều 13 Nghị định 133/2026/NĐ-CP** và liên kết trực tiếp tới từng hóa đơn vi phạm để chủ trọ xử lý ngay.
