import cv2
import config
from mavlink_control import Drone
from vision import Vision

drone = Drone()
vision = Vision()

drone.set_offboard()
drone.arm()
drone.takeoff(config.TAKEOFF_ALT)

print("[INFO] Starting landing loop")

while True:
    frame = vision.get_frame()
    if frame is None:
        continue

    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    pos, frame = vision.detect(frame)

    vx, vy = 0.0, 0.0

    if pos:
        mx, my = pos

        err_x = mx - cx
        err_y = my - cy

        print(f"[TRACK] {err_x}, {err_y}")

        vx = -err_y * config.KP
        vy = -err_x * config.KP

        if abs(err_x) < config.CENTER_THRESHOLD and abs(err_y) < config.CENTER_THRESHOLD:
            print("[SUCCESS] Landing")
            drone.land()
            break

    else:
        print("[WARN] No marker")

    drone.send_velocity(vx, vy, 0.2)

    cv2.imshow("View", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
