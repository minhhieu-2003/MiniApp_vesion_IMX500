# VisionMin.AI

Hệ thống tích hợp cảnh báo tư thế ngồi và chatbot AI bằng giọng nói, tối ưu cho Raspberry Pi (Picamera2). Mục tiêu: hỗ trợ người dùng bằng cảnh báo tư thế bằng tiếng Việt và giao tiếp với AI qua microphone.

## Tổng quan
- Phát hiện tư thế dựa trên MediaPipe, cảnh báo bằng giọng nói (Tiếng Việt).
- Chatbot AI sử dụng API Gemini, kích hoạt bằng hotword và tương tác bằng micro.
- Tích hợp Picamera2 để sử dụng camera module của Raspberry Pi.
- Đồng bộ hóa trạng thái giữa các module để tránh xung đột âm thanh.

## Tính năng chính
- Phát hiện và cảnh báo tư thế ngồi không đúng.
- Chatbot AI kích hoạt bằng hotword ("MỞ CHAT AI") và giao tiếp bằng giọng nói.
- Tạm dừng cảnh báo tư thế khi chatbot đang nói.
- Hỗ trợ điều khiển bàn phím để điều hướng ứng dụng.

## Yêu cầu
- Raspberry Pi (phiên bản hỗ trợ Picamera2) với camera module.
- Microphone hoạt động.
- Python 3.8+.
- Phụ thuộc (cài từ requirements.txt): MediaPipe, Picamera2, thư viện xử lý audio và HTTP client.

## Cài đặt
1. Sao chép repo hoặc đặt mã nguồn vào thư mục dự án:
   ```bash
   cd /d:/Python_Project/picamera2/picamera2/apps
   ```
2. Cài đặt phụ thuộc:
   ```bash
   pip install -r visionmin/requirements.txt
   ```

## Cấu hình API
- KHÔNG nên hardcode API key trong mã nguồn.
- Thiết lập biến môi trường:
  ```bash
  export GEMINI_API_KEY="your-api-key"
  ```
  Hoặc tạo file `.env` trong thư mục chạy ứng dụng:
  ```
  GEMINI_API_KEY=your-api-key
  ```
- Kiểm tra tập tin `config.py` để cấu hình ngưỡng, tham số TTS, và các tùy chọn khác.

## Sử dụng
- Chạy ứng dụng chính:
  ```bash
  python visionmin/app_visionmin.py
  ```
- Phím điều khiển:
  - `q` — thoát ứng dụng
  - `r` — reset bộ đếm/tình trạng tư thế
  - `Ctrl+C` — dừng chương trình

- Hướng dẫn tương tác:
  - Ngồi thẳng, vai cân bằng để tránh cảnh báo.
  - Nói "MỞ CHAT AI" để kích hoạt chatbot.
  - Nói các lệnh như "thoát" hoặc "dừng lại" để tắt chatbot.

## Cấu trúc thư mục
```
visionmin/
├── __init__.py          # Module initialization
├── config.py            # Cấu hình hệ thống (API keys, thresholds)
├── event_bus.py         # Event bus để đồng bộ các module
├── tts_manager.py       # Text-to-Speech manager (gTTS / pyttsx3 wrapper)
├── posture_alert.py     # Phát hiện & cảnh báo tư thế (Picamera2 + MediaPipe)
├── chatbot_ai.py        # Chatbot AI (tương tác với Gemini)
├── requirements.txt     # Các phụ thuộc
└── app_visionmin.py     # Ứng dụng tích hợp các module
```

## Ghi chú vận hành
- Chạy trên Raspberry Pi có kết nối Internet để gọi API Gemini.
- Kiểm tra quyền truy cập microphone và camera trước khi chạy.
- Giữ API key an toàn; nếu chia sẻ mã, loại bỏ hoặc thay thế bằng biến môi trường.

## Đóng góp
- Vui lòng tạo issue trước khi gửi pull request.
- Tuân thủ quy tắc đặt tên, viết unit tests cho tính năng mới và mô tả rõ thay đổi.

## Giấy phép
- Sử dụng theo giấy phép BSD 2-Clause (tùy chỉnh theo repository chính).

Nếu cần, có thể thêm phần hướng dẫn cấu hình chi tiết cho từng nền tảng hoặc script khởi động tự động.
