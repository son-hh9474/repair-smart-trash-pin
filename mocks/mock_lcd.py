import time


class CharLCD:
    """Mock LCD class để giả lập màn hình LCD 16x2 cho testing"""

    def __init__(self, cols=16, rows=2):
        self.cols = cols
        self.rows = rows
        self.cursor_pos = (0, 0)
        self.display_buffer = [[" " for _ in range(cols)] for _ in range(rows)]
        self.is_display_on = True

        print(f"[!] Mock LCD khởi tạo: {cols}x{rows}")
        self._print_lcd_frame()

    def clear(self):
        """Xóa màn hình LCD"""
        self.display_buffer = [
            [" " for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.cursor_pos = (0, 0)
        print("\n[!] LCD cleared")
        self._print_lcd_frame()

    def write_string(self, text):
        """Viết chuỗi text lên LCD tại vị trí cursor hiện tại"""
        row, col = self.cursor_pos

        if row >= self.rows:
            print(f"[!] Cảnh báo: Hàng {row} vượt quá giới hạn LCD ({self.rows} hàng)")
            return

        # Ghi từng ký tự
        for i, char in enumerate(text):
            if col + i < self.cols:
                self.display_buffer[row][col + i] = char
            else:
                break  # Dừng khi vượt quá độ rộng màn hình

        print(f"\nGhi text: '{text}' tại vị trí ({row}, {col})")
        self._print_lcd_frame()

    def _print_lcd_frame(self):
        """In khung LCD giả lập ra console"""
        if not self.is_display_on:
            print("[!] LCD đã tắt")
            return

        # Khung LCD
        border_horizontal = "+" + "-" * (self.cols + 2) + "+"
        print(border_horizontal)
        for row_index, row in enumerate(self.display_buffer):
            row_text = "".join(row)
            print(f"| {row_text} |")
        print(border_horizontal)

    @property
    def cursor_pos(self):
        """Lấy vị trí cursor hiện tại"""
        return self._cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, position):
        """Đặt vị trí cursor (row, col)"""
        row, col = position

        # Kiểm tra giới hạn
        if row >= self.rows:
            row = self.rows - 1
            print(f"[!] Cursor row {position[0]} vượt quá giới hạn, đặt về {row}")
        if col >= self.cols:
            col = self.cols - 1
            print(f"[!] Cursor col {position[1]} vượt quá giới hạn, đặt về {col}")

        self._cursor_pos = (max(0, row), max(0, col))
        print(f"-> Cursor moved to: ({self._cursor_pos[0]}, {self._cursor_pos[1]})")

    def home(self):
        """Đặt cursor về vị trí (0, 0)"""
        self.cursor_pos = (0, 0)
        print("-> Cursor về home (0, 0)")

    def display_enabled(self, enabled=True):
        """Bật/tắt màn hình"""
        self.is_display_on = enabled
        status = "BẬT" if enabled else "TẮT"
        print(f"[!] LCD {status}")
        if enabled:
            self._print_lcd_frame()

    def backlight_enabled(self, enabled=True):
        """Bật/tắt đèn nền (mock)"""
        status = "BẬT" if enabled else "TẮT"
        print(f"[!] Đèn nền LCD {status}")

    def create_char(self, location, pattern):
        """Tạo ký tự tùy chỉnh (mock)"""
        print(f"[!] Tạo ký tự tùy chỉnh tại vị trí {location}")
        print(f"Pattern: {pattern}")

    def write_char(self, char):
        """Viết một ký tự"""
        self.write_string(str(char))

    def shift_display(self, direction="right"):
        """Dịch chuyển nội dung màn hình"""
        direction_arrow = "→" if direction == "right" else "←"
        print(f"[!] Dịch chuyển màn hình {direction_arrow}")
        # Mock implementation - không thực sự dịch chuyển
        self._print_lcd_frame()

    def close(self):
        """Đóng kết nối LCD"""
        self.is_display_on = False
        print("[!] Mock LCD đã đóng kết nối")


# Thêm alias để tương thích với các import khác nhau
MockCharLCD = CharLCD
LCD = CharLCD


if __name__ == "__main__":
    # Tạo LCD mock
    lcd = CharLCD("PCF8574", 0x27, cols=16, rows=2)

    # Test các chức năng
    lcd.write_string("Hello World!")
    time.sleep(1)

    lcd.cursor_pos = (1, 0)
    lcd.write_string("Line 2 Content")
    time.sleep(1)

    lcd.clear()
    lcd.write_string("Thung rac")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("San sang!")

    time.sleep(2)
    lcd.close()
