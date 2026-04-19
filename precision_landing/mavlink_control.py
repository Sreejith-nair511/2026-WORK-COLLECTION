from pymavlink import mavutil
import time
import config

class Drone:
    def __init__(self):
        self.master = mavutil.mavlink_connection(
            config.CONNECTION_STRING, baud=config.BAUD
        )
        self.master.wait_heartbeat()
        print("[INFO] Connected to Pixhawk")

    def send_velocity(self, vx, vy, vz):
        self.master.mav.set_position_target_local_ned_send(
            0,
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0,
            0, 0
        )

    def set_offboard(self):
        for _ in range(20):
            self.send_velocity(0, 0, 0)
            time.sleep(0.1)

        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            self.master.mode_mapping()['OFFBOARD']
        )
        print("[INFO] OFFBOARD mode")

    def arm(self):
        self.master.arducopter_arm()
        self.master.motors_armed_wait()
        print("[INFO] Armed")

    def takeoff(self, alt):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, alt
        )
        print("[INFO] Takeoff")
        time.sleep(5)

    def land(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        print("[INFO] Landing")
