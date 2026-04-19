import time

class FailSafeManager:
    def __init__(self, master):
        self.master = master
        self.last_tag_time = time.time()
        self.last_heartbeat = time.time()
        self.last_frame_time = time.time()
        self.low_battery = False

        self.TAG_TIMEOUT = 2.0
        self.COMM_TIMEOUT = 3.0
        self.FRAME_TIMEOUT = 2.0
        self.BATTERY_THRESHOLD = 20

    def update_tag(self, detected):
        if detected:
            self.last_tag_time = time.time()

    def update_frame(self):
        self.last_frame_time = time.time()

    def update_heartbeat(self):
        self.last_heartbeat = time.time()

    def update_battery(self):
        msg = self.master.recv_match(type='SYS_STATUS', blocking=False)
        if msg:
            if msg.battery_remaining != -1 and msg.battery_remaining < self.BATTERY_THRESHOLD:
                self.low_battery = True

    def check(self):
        now = time.time()

        if now - self.last_frame_time > self.FRAME_TIMEOUT:
            return "CAMERA_FAIL"
        if now - self.last_tag_time > self.TAG_TIMEOUT:
            return "VISION_LOST"
        if now - self.last_heartbeat > self.COMM_TIMEOUT:
            return "COMM_LOST"
        if self.low_battery:
            return "LOW_BATTERY"

        return "OK"

    def execute(self, status):
        if status == "VISION_LOST":
            self._send_hold()
        elif status in ["COMM_LOST", "LOW_BATTERY", "CAMERA_FAIL"]:
            self._set_land_mode()

    def _send_hold(self):
        self.master.mav.landing_target_send(
            int(time.time()*1e6),
            0,
            8,
            0, 0, 0, 0, 0
        )

    def _set_land_mode(self):
        try:
            self.master.set_mode_apm("LAND")
        except:
            print("Failed to switch LAND mode")
