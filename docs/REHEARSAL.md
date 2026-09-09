# Kịch bản Diễn tập Trình diễn RentCalc (15 phút)

Kịch bản phân bổ chi tiết từng giây cho phần thuyết trình và demo trước Hội đồng Ban Giám khảo Olympic Tin học Sinh viên 2026 — Khối Phần mềm Nguồn mở (PMNM).

---

## ⏱️ PHÂN BỔ THỜI GIAN TỔNG THỂ

| Mốc thời gian | Nội dung | Thao tác trên màn hình |
| :--- | :--- | :--- |
| **00:00 – 00:30** | Mở đầu & Giới thiệu đề tài | Slide 1 (Title) |
| **00:30 – 01:30** | Đặt vấn đề thực tế & Cơ sở pháp lý | Slide 2 (Vấn đề & NĐ 133/2026) |
| **01:30 – 03:00** | Giải pháp kỹ thuật & Clean Architecture | Slide 3 – 5 (Kiến trúc 3 tầng & Sơ đồ) |
| **03:00 – 09:00** | Demo trực tiếp hệ thống (7 kịch bản) | Trình duyệt Web (Localhost / Production) |
| **09:00 – 10:30** | Kết quả kiểm thử & Tính bền vững | Slide 11 – 12 (Tests, Coverage, Docs) |
| **10:30 – 11:30** | Hướng phát triển tương lai | Slide 13 (Shared Meter, OCR, Payment) |
| **11:30 – 12:00** | Kết luận | Slide 14 (Giá trị xã hội của PMNM) |
| **12:00 – 15:00** | Hỏi & Đáp (Q&A) | Slide 15 (Sẵn sàng trả lời BGK) |

---

## 🎤 LỜI THOẠI VÀ THAO TÁC CHI TIẾT TỪNG PHÚT

### 00:00 – 00:30 — Mở đầu
- **Lời thoại:**  
  *"Kính thưa Ban Giám khảo và các thầy cô, em tên là Trần Vũ Hoa Phát, sinh viên tham dự Olympic Tin học Sinh viên 2026 khối Phần mềm Nguồn mở. Hôm nay, em xin được trình bày dự án **RentCalc** — Hệ thống quản trị và minh bạch hóa chi phí dịch vụ điện nước sinh hoạt phòng trọ theo quy chuẩn Nhà nước."*
- **Hành động:** Chiếu Slide 1.

---

### 00:30 – 01:30 — Vấn đề thực tế
- **Lời thoại:**  
  *"Hiện nay tại các đô thị lớn, hàng triệu sinh viên và người lao động thuê trọ đang phải gánh chịu mức thu điện khoán từ 3.500 đến 4.500 đồng/kWh — cao hơn cả bậc thang lũy tiến cao nhất của Nhà nước.  
  Mặc dù Điều 31 Nghị định 133/2026/NĐ-CP đã quy định chế tài xử phạt từ 20 đến 30 triệu đồng đối với hành vi thu vượt biểu giá, nhưng người thuê thường không có công cụ tính toán đối chiếu, còn chủ nhà trọ thì ngại tính toán bậc thang phức tạp cho từng phòng.  
  RentCalc ra đời nhằm giải quyết triệt để bài toán này bằng công nghệ phần mềm nguồn mở."*
- **Hành động:** Chiếu Slide 2.

---

### 01:30 – 03:00 — Giải pháp kỹ thuật & Kiến trúc Clean Architecture
- **Lời thoại:**  
  *"Về mặt kỹ thuật, RentCalc được xây dựng theo mô hình **Clean Layered Architecture** tách bạch 3 tầng độc lập:  
  1. **Core Calculation Engine:** Thuần Python, không phụ thuộc bất kỳ framework web hay database nào. Toàn bộ phép toán tài chính được thực hiện bằng thư viện `Decimal` với độ chính xác tuyệt đối, không có sai số dấu phẩy động (zero float loss).  
  2. **Database Layer:** Sử dụng PostgreSQL 16 và SQLAlchemy 2.0, lưu trữ hóa đơn dưới dạng snapshot bất biến — nghĩa là khi biểu giá tương lai thay đổi, các hóa đơn cũ vẫn giữ nguyên vẹn giá trị lịch sử.  
  3. **Web & UI Layer:** FastAPI tốc độ cao kết hợp Jinja2 Templates và Tailwind CSS, hỗ trợ đầy đủ tiêu chuẩn tiếp cận a11y và responsive trên mọi thiết bị di động."*
- **Hành động:** Chiếu Slide 4 và Slide 5 (sơ đồ Mermaid).

---

### 03:00 – 09:00 — DEMO TRỰC TIẾP TRÊN TRÌNH DUYỆT (6 PHÚT)

*(Chuyển sang cửa sổ trình duyệt `http://127.0.0.1:8000`)*

#### Demo 1: Đăng nhập Chủ cơ sở (03:00 – 03:30)
- **Lời thoại:** *"Trước hết, em đăng nhập bằng tài khoản Chủ trọ `owner / owner123`. Sau khi đăng nhập, hệ thống gắn session bảo mật và hiển thị Bảng điều khiển tổng quan với đầy đủ thống kê số cơ sở, số phòng và số hóa đơn đã phát hành."*
- **Hành động:** Đăng nhập, mở Dashboard, trỏ chuột vào 4 thẻ chỉ số và Navbar có tên `Chủ trọ`.

#### Demo 2: Kiểm thử TC-01 — Tính hóa đơn phòng 4 người (03:30 – 04:30)
- **Lời thoại:** *"Bây giờ em tạo hóa đơn cho Phòng 101 với 4 người ở, tiêu thụ 120 kWh điện và 16 m³ nước. Nhờ cơ chế chia định mức theo nhân khẩu, 120 kWh điện này được tính trọn vẹn trong Bậc 1 (mỗi người 50 kWh định mức, tổng 200 kWh ở Bậc 1). Tiền điện tính ra đúng 269.244 đồng, khớp chính xác 100% từng đồng với kết quả đề bài."*
- **Hành động:** Vào danh sách hóa đơn, mở chi tiết hóa đơn Phòng 101, chỉ vào bảng bóc tách lũy tiến từng bậc.

#### Demo 3: Kiểm thử TC-04 — Công tơ quay vòng (Rollover) (04:30 – 05:30)
- **Lời thoại:** *"Trong thực tế, công tơ cơ khí khi chạy hết 99999 sẽ quay vòng về 00000. Tại form ghi chỉ số, em nhập số cũ 99.850 và số mới 00.120. Ngay lập tức, hệ thống kích hoạt cảnh báo màu vàng Rollover và tự động áp dụng công thức modulo để xác định chính xác sản lượng tiêu thụ là 270 kWh, tính ra 701.525 đồng."*
- **Hành động:** Mở form chốt chỉ số công tơ, gõ số 99850 và 120, cho BGK thấy banner cảnh báo Rollover tự động hiện ra.

#### Demo 4: Xuất Hóa đơn điện tử PDF chuẩn (05:30 – 06:00)
- **Lời thoại:** *"Em bấm nút '📄 PDF' để xuất hóa đơn chính thức. Hệ thống xử lý render trực tiếp qua stream bộ nhớ, đảm bảo 100% font tiếng Việt có dấu sắc nét, bảng tính và chữ ký được căn giữa chuẩn mực theo quy cách kế toán."*
- **Hành động:** Bấm nút PDF, mở file PDF trong tab mới, cuộn qua bảng bóc tách và dòng tổng tiền bằng chữ.

#### Demo 5: Chia sẻ minh bạch không cần đăng nhập (06:00 – 07:00)
- **Lời thoại:** *"Chủ nhà có thể gửi đường link chia sẻ có mã token bảo mật cho người thuê. Em copy link `/share/...`, mở một tab ẩn danh hoàn toàn không đăng nhập. Người thuê có thể tự mình kiểm tra bảng bóc tách và tải PDF về máy bất cứ lúc nào."*
- **Hành động:** Mở tab Incognito, dán link `/share/demo-token-101`, chứng minh không cần login vẫn xem được bảng minh bạch.

#### Demo 6: Đăng nhập Khách thuê phòng (07:00 – 08:00)
- **Lời thoại:** *"Bây giờ em đăng xuất tài khoản Chủ trọ và đăng nhập bằng tài khoản Khách thuê `tenant101 / tenant123`. Hệ thống nhận diện vai trò `tenant`, tự động chuyển hướng vào trang 'Hóa đơn của tôi', chỉ hiển thị các hóa đơn của Phòng 101 và ẩn toàn bộ các chức năng quản trị cơ sở."*
- **Hành động:** Đăng nhập `tenant101`, xem giao diện `/my-invoices`.

#### Demo 7: Cảnh báo vi phạm Nghị định 133/2026/NĐ-CP (08:00 – 09:00)
- **Lời thoại:** *"Khi chủ trọ nhập mức thu khoán 4.000 đ/kWh, số tiền thực thu là 480.000 đồng, cao hơn giá quy định 269.244 đồng. Ngay trên Bảng điều khiển, banner cảnh báo màu đỏ nổi bật kích hoạt, nêu rõ hành vi vi phạm Điều 31 Nghị định 133 với mức phạt 20-30 triệu đồng và chỉ rõ số tiền thu vượt 210.756 đồng cần hoàn trả."*
- **Hành động:** Quay lại Dashboard chủ trọ, trỏ vào banner cảnh báo pháp lý đỏ.

---

### 09:00 – 10:30 — Kết quả Kiểm thử & Tính Bền vững
- **Lời thoại:**  
  *"Về mặt chất lượng phần mềm, dự án RentCalc đã vượt qua **51/51 automated tests (100%)** với độ phủ mã nguồn đạt **85%**.  
  Dự án cung cấp bộ tài liệu đầy đủ từ cài đặt nguồn (`INSTALL.md`), hướng dẫn chạy kịch bản demo (`DEMO.md`), đến hướng dẫn triển khai production (`DEPLOY.md`) bằng Docker Compose và Nginx reverse proxy."*
- **Hành động:** Chiếu Slide 11 và Slide 12.

---

### 10:30 – 11:30 — Phương hướng phát triển tương lai
- **Lời thoại:**  
  *"Trong các phiên bản tiếp theo, RentCalc sẽ tiếp tục phát triển:  
  1. Hỗ trợ mô hình công tơ tổng chia cho nhiều phòng chung (Shared Meter Topology).  
  2. Thuật toán xử lý khi Nhà nước điều chỉnh giá điện giữa kỳ thanh toán.  
  3. Ứng dụng di động quét ảnh công tơ bằng trí tuệ nhân tạo OCR và tích hợp thanh toán mã VietQR."*
- **Hành động:** Chiếu Slide 13.

---

### 11:30 – 12:00 — Kết luận
- **Lời thoại:**  
  *"Tóm lại, RentCalc không chỉ là một bài toán kỹ thuật mà còn là một công cụ mã nguồn mở mang lại giá trị xã hội thiết thực, bảo vệ quyền lợi chính đáng của người đi thuê và thúc đẩy văn hóa sống minh bạch, tuân thủ pháp luật.  
  Em xin trân trọng cảm ơn Ban Giám khảo đã chú ý theo dõi!"*
- **Hành động:** Chiếu Slide 14 và Slide 15.

---

### 12:00 – 15:00 — Hỏi & Đáp (Q&A)
- Chuẩn bị sẵn terminal và code để giải thích chi tiết:
  - Cơ chế tính `Decimal` chống sai số tại `app/core/electricity.py`.
  - Thuật toán định mức lũy tiến tại `app/core/quota.py`.
  - Phân quyền RBAC tại `app/auth.py`.
  - Xử lý Unicode PDF tại `app/services/pdf_service.py`.
