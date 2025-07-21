import random

class MotionSensor:
    def __init__(self, pin=None):
        self.pin = pin
        self._motion_detected = False
        self._person_simulation = False
        
    @property
    def motion_detected(self):
        """Giả lập PIR phát hiện chuyển động của người"""
        if self._person_simulation:
            # 80% khả năng phát hiện khi có người
            return random.random() < 0.8
        return self._motion_detected
    
    def simulate_person_presence(self, present=True):
        """Giả lập có người hiện diện"""
        self._person_simulation = present
        self._motion_detected = present
    
    def simulate_object_only(self):
        """Giả lập chỉ có vật thể (không chuyển động)"""
        self._person_simulation = False
        self._motion_detected = False

class DistanceSensor:
    def __init__(self, echo=None, trigger=None):
        self.echo = echo
        self.trigger = trigger
        self._distance = 3.0
        self._object_type = "person"  # "person" hoặc "object"
        
    @property
    def distance(self):
        """Giả lập khoảng cách với độ nhiễu nhỏ"""
        noise = random.uniform(-0.1, 0.1)
        return max(0.1, self._distance + noise)
    
    def simulate_person_at_distance(self, distance):
        """Giả lập người ở khoảng cách cụ thể"""
        self._distance = distance
        self._object_type = "person"
    
    def simulate_object_at_distance(self, distance):
        """Giả lập vật thể ở khoảng cách cụ thể"""
        self._distance = distance
        self._object_type = "object"

class Servo:
    def __init__(self, pin):
        self.pin = pin
        self._position = -1  # -1: đóng, 1: mở
        
    def max(self):
        self._position = 1
        print(f"🔧 Servo pin {self.pin}: MỞ nắp")
    
    def min(self):
        self._position = -1
        print(f"🔧 Servo pin {self.pin}: ĐÓNG nắp")

# Alias để tương thích
MockPIRSensor = MotionSensor