from unittest import TestCase
from smart_trash_bin import SmartTrashBin


class TestTrashBin(TestCase):
    """
    | Tình huống	    | PIR	                | Distance | Kết quả      |
    |-------------------|-----------------------|----------|--------------|
    | Người ở 1.5m	    | [x] Có chuyển động    | [x] ≤ 2m | [x] MỞ NẮP   |
    | Vật thể ở 1.5m	| [ ] Không chuyển động | [x] ≤ 2m | [ ] Không mở |
    | Người ở 3m	    | [x] Có chuyển động	| [ ] > 2m | [ ] Không mở |
    | Không có gì	    | [ ] Không chuyển động | [ ] > 2m | [ ] Không mở |
    """

    def setUp(self):
        """
        Thiết lập cảm biến của thùng rác, khoảng cách kích hoạt, thời gian dừng, chờ
        """
        self.trash_bin = SmartTrashBin(trigger_distance=2.0, hold_time=2)

    def test_person_nearby_opens_lid(self):
        """Có người gần thì mở nắp"""
        # Giả lập người ở 1.5m
        self.trash_bin.distance_sensor.simulate_person_at_distance(1.5)
        self.trash_bin.pir_sensor.simulate_person_presence(True)

        person_nearby, _, _ = self.trash_bin._is_person_nearby()

        # Cần chạy vài lần để xác nhận
        for _ in range(5):
            person_nearby, _, _ = self.trash_bin._is_person_nearby()

        self.assertTrue(person_nearby)

    def test_object_nearby_does_not_open_lid(self):
        """Chỉ có vật thể gần thì KHÔNG mở nắp"""
        # Giả lập vật thể ở 1.5m (không có người)
        self.trash_bin.distance_sensor.simulate_object_at_distance(1.5)
        self.trash_bin.pir_sensor.simulate_object_only()

        for _ in range(5):
            person_nearby, _, _ = self.trash_bin._is_person_nearby()

        self.assertFalse(person_nearby)

    def test_person_far_away_does_not_trigger(self):
        """Người ở xa thì không kích hoạt"""
        # Giả lập người ở 3m (xa hơn ngưỡng 2m)
        self.trash_bin.distance_sensor.simulate_person_at_distance(3.0)
        self.trash_bin.pir_sensor.simulate_person_presence(True)

        for _ in range(5):
            person_nearby, _, _ = self.trash_bin._is_person_nearby()

        self.assertFalse(person_nearby)
