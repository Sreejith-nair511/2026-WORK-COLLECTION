import cv2
import numpy as np
import os

# =========================
# CONFIG
# =========================
MARKER_ID = 0
MARKER_SIZE = 500

# =========================
# LOAD DICTIONARY (NEW API)
# =========================
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# =========================
# GENERATE MARKER
# =========================
marker_file = f"aruco_{MARKER_ID}.png"

if not os.path.exists(marker_file):
    marker = cv2.aruco.generateImageMarker(aruco_dict, MARKER_ID, MARKER_SIZE)
    cv2.imwrite(marker_file, marker)
    print(f"[INFO] Marker generated: {marker_file}")
else:
    print(f"[INFO] Marker exists: {marker_file}")

# =========================
# DETECTOR SETUP (NEW API)
# =========================
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    print("[ERROR] Camera not opening")
    exit()

print("[INFO] Show marker to camera. Press ESC to exit.")

# =========================
# LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Frame issue")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        print("[SUCCESS] Detected:", ids.flatten())

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i in range(len(ids)):
            c = corners[i][0]
            cx = int(c[:, 0].mean())
            cy = int(c[:, 1].mean())

            cv2.putText(frame,
                        f"ID: {ids[i][0]}",
                        (cx, cy),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2)
    else:
        print(f"[DEBUG] No detection | rejected: {len(rejected)}")

    cv2.imshow("Aruco Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()