#!/usr/bin/env python3

# ─────────────────────────────────────────────
# ENV SETUP (for Raspberry Pi display issues)
# ─────────────────────────────────────────────
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'
os.environ['DISPLAY'] = ':0'

# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
import cv2
import numpy as np
import time
from picamera2 import Picamera2
from pupil_apriltags import Detector

# ─────────────────────────────────────────────
# CONFIGURATION (TUNE THESE CAREFULLY)
# ─────────────────────────────────────────────
WIDTH, HEIGHT = 1280, 720        # Balanced resolution
TAG_SIZE = 0.30                  # meters (IMPORTANT: real size)
FX, FY = 900, 900                # focal lengths (approx)
CX, CY = WIDTH // 2, HEIGHT // 2

CAM_PARAMS = (FX, FY, CX, CY)

# Detection tuning (for long distance)
detector = Detector(
    families="tag36h11",
    nthreads=4,
    quad_decimate=1.5,
    quad_sigma=0.8,
    refine_edges=1,
    decode_sharpening=0.5
)

# ─────────────────────────────────────────────
# CAMERA SETUP
# ─────────────────────────────────────────────
picam = Picamera2()

config = picam.create_preview_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
)

picam.configure(config)
picam.start()

time.sleep(2)

# ─────────────────────────────────────────────
# SMOOTHING FILTER (reduces pose jitter)
# ─────────────────────────────────────────────
alpha = 0.6
prev_pose = None

def smooth_pose(tvec):
    global prev_pose
    if prev_pose is None:
        prev_pose = tvec
        return tvec
    smoothed = alpha * prev_pose + (1 - alpha) * tvec
    prev_pose = smoothed
    return smoothed

# ─────────────────────────────────────────────
# FPS CALCULATION
# ─────────────────────────────────────────────
prev_time = time.time()
fps = 0

# ─────────────────────────────────────────────
# WINDOW
# ─────────────────────────────────────────────
cv2.namedWindow("AprilTag Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("AprilTag Detection", 1280, 720)

print("========================================")
print(" AprilTag Detection Running")
print(" Target range: ~5 meters (depends on tag size)")
print(" Press Q to quit")
print("========================================")

# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
while True:

    frame = picam.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    display = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    h, w = gray.shape

    # ───────── DETECTION ─────────
    tags = detector.detect(
        gray,
        estimate_tag_pose=True,
        camera_params=CAM_PARAMS,
        tag_size=TAG_SIZE
    )

    # ───────── DRAW RESULTS ─────────
    if tags:
        for tag in tags:

            corners = tag.corners.astype(int)
            cx, cy = int(tag.center[0]), int(tag.center[1])

            # Draw bounding box
            cv2.polylines(display, [corners], True, (0, 255, 0), 2)

            # Draw center
            cv2.circle(display, (cx, cy), 6, (0, 255, 0), -1)

            # Pose
            tx, ty, tz = tag.pose_t.flatten()
            tx, ty, tz = smooth_pose(np.array([tx, ty, tz]))

            # Draw direction vector
            cv2.line(display, (w//2, h//2), (cx, cy), (255, 0, 0), 2)

            # Overlay text
            cv2.putText(display,
                        f'ID:{tag.tag_id}',
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2)

            cv2.putText(display,
                        f'X:{tx:.2f}m Y:{ty:.2f}m Z:{tz:.2f}m',
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2)

            cv2.putText(display,
                        f'Offset: ({cx - w//2}, {cy - h//2})',
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 200, 255),
                        2)

            print(f"[Tag {tag.tag_id}] X:{tx:.2f} Y:{ty:.2f} Z:{tz:.2f}m", end="\r")

    else:
        cv2.putText(display,
                    "NO TAG DETECTED",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    2)

    # ───────── CROSSHAIR ─────────
    cv2.drawMarker(display,
                   (w//2, h//2),
                   (0, 0, 255),
                   cv2.MARKER_CROSS,
                   30,
                   2)

    # ───────── FPS ─────────
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(display,
                f'FPS: {fps:.1f}',
                (w - 150, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2)

    # ───────── DISPLAY ─────────
    cv2.imshow("AprilTag Detection", display)

    # ───────── EXIT ─────────
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ─────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────
picam.stop()
cv2.destroyAllWindows()