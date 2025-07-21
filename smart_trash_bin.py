from time import sleep

from config import TRASH_PIN_DISTANCE_ECHO, TRASH_PIN_DISTANCE_TRIGGER, TRASH_PIN_MOTION

try:
    from gpiozero import DistanceSensor, MotionSensor, Servo
    from RPLCD.i2c import CharLCD
# Trong trường hợp không thể import gpiozero (chạy môi trường khác Raspberry) sử dụng mock object
except Exception as _:
    from mocks.mock_gpiozero import DistanceSensor, MotionSensor, Servo
    from mocks.mock_lcd import CharLCD


class SmartTrashBin:
    def __init__(self, trigger_distance=2.0, hold_time=5):
        # Thiết lập các chân cảm biến
        # Khai báo cảm biến siêu âm với max_distance và threshold_distance
        self.max_range = 4.0
        self.distance_sensor = DistanceSensor(
            echo=TRASH_PIN_DISTANCE_ECHO,
            trigger=TRASH_PIN_DISTANCE_TRIGGER,
            max_distance=self.max_range,
            #threshold_distance=trigger_distance,
            queue_len=5,
            partial=True
        )
        
        self.pir_sensor = MotionSensor(TRASH_PIN_MOTION)

        # Servo điều khiển nắp
        self.lid_servo = Servo(18)

        # LCD hiển thị
        self.lcd = CharLCD(cols=16, rows=2)

        # Cấu hình
        self.trigger_distance = trigger_distance  # 2m
        self.hold_time = hold_time

        # Trạng thái
        self.is_lid_open = False
        self.monitoring = True
        self.person_detection_history = []  # Lưu lịch sử phát hiện

        # Khởi tạo
        self._close_lid()
        self._display_status("Thung rac thong minh", "San sang phuc vu")

    def _is_person_nearby(self):
        """
        Kiểm tra có NGƯỜI gần không (sử dụng kết hợp PIR + distance)
        """
        # Kiểm tra chuyển động (PIR)
        motion_detected = self.pir_sensor.motion_detected

        # Đo khoảng cách
        distance = self.distance_sensor.distance * self.max_range

        # Điều kiện: Có chuyển động AND khoảng cách <= 2m
        person_nearby = motion_detected and (distance <= self.trigger_distance)

        # Lưu lịch sử để tránh false positive
        self.person_detection_history.append(person_nearby)
        if len(self.person_detection_history) > 5:  # Chỉ giữ 5 lần đo gần nhất
            self.person_detection_history.pop(0)

        # Reset nếu 5 lần đều False (không thấy ai)
        if len(self.person_detection_history) == 5 and all(not x for x in self.person_detection_history):
            self.person_detection_history.clear()

        # Xác nhận: ít nhất 3/5 lần gần đây phát hiện người
        confirmed_detection = sum(self.person_detection_history) >= 3

        return confirmed_detection, distance, motion_detected

    def _open_lid(self):
        """Mở nắp thùng rác"""
        if not self.is_lid_open:
            self.lid_servo.max()
            self.is_lid_open = True
            self.person_detection_history.clear()
            self._display_status("Chao ban!", "Hay bo rac vao")
            print("Nắp thùng rác MỞ - Phát hiện NGƯỜI")

    def _close_lid(self):
        """Đóng nắp thùng rác"""
        if self.is_lid_open:
            self.lid_servo.min()
            self.is_lid_open = False
            self._display_status("Cam on ban!", "Hen gap lai")
            print("Nắp thùng rác ĐÓNG")

    def _display_status(self, line1, line2=""):
        """Hiển thị trạng thái"""
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(line1[:16])
        if line2:
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(line2[:16])

    def _display_debug_info(self, distance, motion, person_confirmed):
        """Hiển thị thông tin debug"""
        motion_icon = "👤" if motion else "❌"
        distance_status = f"{distance:.1f}m"
        person_status = "NGƯỜI" if person_confirmed else "VẬT THỂ"

        print(
            f"{motion_icon} Chuyển động: {motion} | 📏 Khoảng cách: {distance_status} | 🎯 Kết luận: {person_status}"
        )

    def run(self):
        """Kích hoạt chạy cảm biến thùng rác đóng/mở"""
        print("Thùng rác thông minh (PIR + Siêu âm) đã khởi động!")
        print(f"Khoảng cách kích hoạt: {self.trigger_distance}m")
        print("Chỉ mở nắp khi phát hiện NGƯỜI (không phải vật thể)")

        no_person_time = 0

        try:
            while self.monitoring:
                person_nearby, distance, motion = self._is_person_nearby()

                # Debug info
                self._display_debug_info(distance, motion, person_nearby)

                if person_nearby:
                    # Có người gần -> mở nắp
                    if not self.is_lid_open:
                        self._open_lid()
                    no_person_time = 0  # Reset timer

                else:
                    # Không có người
                    if self.is_lid_open:
                        no_person_time += 0.5
                        remaining_time = self.hold_time - no_person_time

                        if remaining_time > 0:
                            self._display_status(
                                "Dang dong nap...", f"Con {remaining_time:.0f}s"
                            )
                        else:
                            self._close_lid()
                            no_person_time = 0
                    else:
                        self._display_status(
                            "Cho nguoi den...", f"Pham vi: {self.trigger_distance}m"
                        )

                sleep(0.5)

        except KeyboardInterrupt:
            # Nếu bấm phím gì đó thì tắt thùng rác
            # TODO: Triển khai công tắc đóng/mở
            self.stop()

    def stop(self):
        """Dừng hoạt động"""
        self.monitoring = False
        self._close_lid()
        self._display_status("Da tam dung")
        print("\nThùng rác đã dừng")


if __name__ == "__main__":
    trash_bin = SmartTrashBin(trigger_distance=2.0, hold_time=5)
    trash_bin.run()
