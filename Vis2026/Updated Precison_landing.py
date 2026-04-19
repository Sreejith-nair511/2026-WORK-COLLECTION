# precisionland.py — FINAL DRONE-READY VERSION

import time
import math
import threading
import logging
import numpy as np
import cv2

from pymavlink import mavutil
from pupil_apriltags import Detector

logger = logging.getLogger(__name__)

# ───────────────── CONFIG ─────────────────
CAM_WIDTH = 1280
CAM_HEIGHT = 720

# REAL CAMERA PARAMS (CALIBRATE LATER)
FX = 900
FY = 900
CX = CAM_WIDTH // 2
CY = CAM_HEIGHT // 2

TAG_SIZE = 0.30  # meters

SEND_RATE_HZ = 15
EMA_ALPHA = 0.4
DEADBAND = 0.02
MIN_TAG_AREA = 600

# ─────────────────────────────────────────

class PrecisionLander:
    def __init__(self, vehicle, camera):
        self.vehicle = vehicle
        self.camera = camera
        self.running = False

        # smoothing
        self.tx_f = 0
        self.ty_f = 0
        self.tz_f = 0

        # detector (HIGH QUALITY)
        self.detector = Detector(
            families="tag36h11",
            nthreads=4,
            quad_decimate=1.5,
            quad_sigma=0.8,
            refine_edges=1,
            decode_sharpening=0.5
        )

        self.master = mavutil.mavlink_connection(
            vehicle._master.address
        )

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False

    def _smooth(self, val, prev):
        return EMA_ALPHA * val + (1 - EMA_ALPHA) * prev

    def _run(self):
        while self.running:

            frame = self.camera.capture_array()
            if frame is None:
                time.sleep(0.05)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            tags = self.detector.detect(
                gray,
                estimate_tag_pose=True,
                camera_params=(FX, FY, CX, CY),
                tag_size=TAG_SIZE
            )

            if tags:
                tag = max(tags, key=lambda t: t.decision_margin)

                # Pose (meters)
                tx, ty, tz = tag.pose_t.flatten()

                # Smooth pose
                self.tx_f = self._smooth(tx, self.tx_f)
                self.ty_f = self._smooth(ty, self.ty_f)
                self.tz_f = self._smooth(tz, self.tz_f)

                # Convert to angles (critical for MAVLink)
                angle_x = math.atan2(self.tx_f, self.tz_f)
                angle_y = math.atan2(self.ty_f, self.tz_f)

                # Deadband
                if abs(angle_x) < DEADBAND:
                    angle_x = 0
                if abs(angle_y) < DEADBAND:
                    angle_y = 0

                # Send to flight controller
                self._send_landing_target(angle_x, angle_y)

                logger.info(
                    f"[PL] X:{self.tx_f:.2f} Y:{self.ty_f:.2f} Z:{self.tz_f:.2f}m"
                )

            time.sleep(1 / SEND_RATE_HZ)

    def _send_landing_target(self, angle_x, angle_y):
        self.master.mav.landing_target_send(
            int(time.time() * 1e6),
            0,
            mavutil.mavlink.MAV_FRAME_BODY_FRD,
            angle_x,
            angle_y,
            0,
            0,
            0
        )