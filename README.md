## Dự án

Một chương trình IoT nhỏ dùng để phát hiện người đến gần thùng rác, khi người đến gần, chương trình sẽ kích hoạt motor để điều khiển nắp thùng rác, cho phép thùng rác tự động đóng/mở

## Phần cứng

Gồm các loại phần cứng sau

- **Raspberry Pi**: Vi điều khiển chính
- **HC-SR04**: Cảm biến siêu âm đo khoảng cách (mặc định là 2m)
- **PIR HC-SR501**: Cảm biến chuyển động hồng ngoại (dùng để phát hiện người)
- **SG90**: Servo motor điều khiển nắp _(dự tính chưa triển khai xong)_
- **LCD 16x2 I2C**: Màn hình hiển thị trạng thái _(dự tính, chưa triển khai xong)_

## Cấu trúc dự án

```
pir-presence-detector/
├── smart_trash_bin.py        # Logic chính của thùng rác
├── main.py                   # Entry point chạy ứng dụng
├── config.py                 # Cấu hình chân GPIO
├── mocks/                    # Mock objects cho test
│   ├── mock_gpiozero.py      # Giả lập cảm biến GPIO
│   └── mock_lcd.py           # Giả lập màn hình LCD
├── tests/                    # Test cases
│   └── test_trash_bin.py     # Unit tests cho thùng rác
└── requirements.txt          # Dependencies
```

## Chức năng

- **Phát hiện người và tự động mở nắp**: Kết hợp PIR + cảm biến siêu âm HC-SR04, chỉ mở khi có người trong phạm vi 2m
- **Hiển thị LCD**: Thông báo trạng thái và chào mừng
- **Mock objects**: Test được mà không cần phần cứng

## Cài đặt và chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
# Chạy thùng rác
python main.py

# Hoặc chạy trực tiếp
python smart_trash_bin.py
```

### 3. Chạy test

```bash
# Chạy tất cả test
python -m unittest discover tests -v

# Hoặc chạy file test cụ thể
python -m unittest tests.test_trash_bin -v
```

## Logic hoạt động

| Tình huống     | PIR                  | Khoảng cách | Kết quả       |
| -------------- | -------------------- | ----------- | ------------- |
| Người ở 1.5m   | ✅ Có chuyển động    | ✅ ≤ 2m     | ✅ **MỞ NẮP** |
| Vật thể ở 1.5m | ❌ Không chuyển động | ✅ ≤ 2m     | ❌ Không mở   |
| Người ở 3m     | ✅ Có chuyển động    | ❌ > 2m     | ❌ Không mở   |
| Không có gì    | ❌ Không chuyển động | ❌ > 2m     | ❌ Không mở   |

## Ghi chú

- Nhấn `Ctrl+C` để dừng chương trình
- Cấu hình chân GPIO trong file [`config.py`](config.py)
