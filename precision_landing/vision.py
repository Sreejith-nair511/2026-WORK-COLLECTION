import cv2
import config

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(3, config.FRAME_WIDTH)
        self.cap.set(4, config.FRAME_HEIGHT)

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )
        self.detector = cv2.aruco.ArucoDetector(
            self.aruco_dict, cv2.aruco.DetectorParameters()
        )

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)

        if ids is None:
            return None, frame

        c = corners[0][0]
        mx = int(c[:, 0].mean())
        my = int(c[:, 1].mean())

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        return (mx, my), frame
