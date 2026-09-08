# Kịch bản Demo 7 Trường hợp Kiểm thử Chính thức (TC01 – TC07)

Tài liệu này hướng dẫn thao tác trên giao diện Web RentCalc để kiểm chứng tính đúng đắn và tính minh bạch.

---

## Chuẩn bị

Truy cập: http://localhost:8000/properties -> chọn "Nhà trọ Mẫu TP.HCM".

---

## Kịch bản 1: Phòng đã kê khai số người (Biểu giá bậc thang có định mức)

- Đối tượng: Phòng 101 (4 người -> 1 định mức hộ theo TT 60/2025/TT-BCT).

1. Vào chi tiết Phòng 101 -> bấm "+ Nhập chỉ số công tơ".
2. Điện: Tháng 2026-09, số đầu 0, số cuối 120 (Tiêu thụ 120 kWh).
3. Nước: Tháng 2026-09, số đầu 0, số cuối 16 (Tiêu thụ 16 m3).
4. Quay lại trang phòng -> mục Phát hành hóa đơn, chọn tháng 2026-09 -> bấm "Tính tiền & Xuất hóa đơn".
5. Kiểm tra kết quả bóc tách:
   - Bậc 1 (50 kWh): 99.200 đ
   - Bậc 2 (50 kWh): 102.500 đ
   - Bậc 3 (20 kWh): 47.600 đ
   - Tiền điện có VAT 8%: 268.812 đ
   - Tiền nước (16 m3 có VAT 5% & BVMT 10%): 156.400 đ
   - Tổng cộng theo luật: 425.212 đ.
6. Đối chiếu thực thu:
   - Nhập số tiền chủ nhà thu: 500000 -> Bấm "Đối chiếu chênh lệch".
   - Hệ thống hiển thị khung đỏ cảnh báo: Thu vượt 74.788 đ kèm cảnh báo phạt vi phạm 20–30 triệu đồng theo Điều 31 Nghị định 133/2026/NĐ-CP!

---

## Kịch bản 2: Phòng không kê khai tạm trú (Áp đồng giá Bậc 3)

- Đối tượng: Phòng 102 (Không kê khai tạm trú).

1. Vào chi tiết Phòng 102 -> ghi số điện: 0 đến 100 (100 kWh).
2. Phát hành hóa đơn tháng 2026-09.
3. Kiểm tra kết quả: Toàn bộ 100 kWh bị áp đồng giá Bậc 3 (2.380 đ/kWh) -> Tiền điện sau thuế 8%: 257.040 đ.
