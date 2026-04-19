import time
import math
import cv2
import numpy as np

from pymavlink import mavutil
from picamera2 import Picamera2
from pupil_apriltags import Detector
from failsafe import FailSafeManager

WIDTH, HEIGHT = 1280, 720
TAG_SIZE = 0.30

FX, FY = 900, 900
CX, CY = WIDTH//2, HEIGHT//2

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 115200

DESCENT_SPEED = 0.3
LAND_ALTITUDE = 0.5

master = mavutil.mavlink_connection(SERIAL_PORT, baud=BAUD)
master.wait_heartbeat()

picam = Picamera2()
config = picam.create_preview_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
)
picam.configure(config)
picam.start()
time.sleep(2)

detector = Detector(families="tag36h11")

failsafe = FailSafeManager(master)

def get_altitude():
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
    if msg:
        return msg.relative_alt / 1000.0
    return None

def send_velocity(vx, vy, vz):
    master.mav.set_position_target_local_ned_send(
        int(time.time()*1e6),
        0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        0, 0
    )

def set_land_mode():
    master.set_mode_apm("LAND")

while True:
    frame = picam.capture_array()
    failsafe.update_frame()

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    tags = detector.detect(
        gray,
        estimate_tag_pose=True,
        camera_params=(FX, FY, CX, CY),
        tag_size=TAG_SIZE
    )

    detected = len(tags) > 0
    failsafe.update_tag(detected)
    failsafe.update_battery()

    hb = master.recv_match(type='HEARTBEAT', blocking=False)
    if hb:
        failsafe.update_heartbeat()

    status = failsafe.check()

    if status != "OK":
        failsafe.execute(status)
        continue

    altitude = get_altitude()

    if detected and altitude is not None:
        tag = tags[0]
        tx, ty, tz = tag.pose_t.flatten()

        vx = -tx
        vy = -ty

        if altitude > LAND_ALTITUDE:
            vz = DESCENT_SPEED
        else:
            set_land_mode()
            break

        send_velocity(vx, vy, vz)

    else:
        send_velocity(0, 0, 0)

    time.sleep(0.05)
