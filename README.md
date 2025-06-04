# Ứng dụng Xem Tử Vi Bắc Phái

## Hướng dẫn sử dụng

1. Cài đặt Python 3.x.
2. Cài Flask:
   ```
   pip install flask flask_cors
   ```
3. Chạy ứng dụng:
   ```
   python app.py
   ```
4. Truy cập [http://localhost:5000](http://localhost:5000) để sử dụng giao diện.

## Chức năng

- Nhập thông tin cá nhân, ngày tháng năm sinh, chọn loại lịch.
- Nếu chọn dương lịch, hệ thống sẽ tự động chuyển sang âm lịch trước khi cho phép xem tử vi.
- Mã nguồn chuyển đổi lịch hoàn toàn không phụ thuộc thư viện ngoài.