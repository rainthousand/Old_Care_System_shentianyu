import time

import cv2
from event_ws import event_handle
import threading


class VideoCamera(object):
    def __init__(self):
        # 打开摄像头， 0代表笔记本内置摄像头
        self.cap = cv2.VideoCapture(0)

    # 退出程序释放摄像头
    def __del__(self):
        self.cap.release()

    def get_real_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # frame = event_handle.detect_smile(frame)
            # frame = event_handle.detect_fall(frame)
            # frame = event_handle.detect_invasion(frame,self.first_frame())

            ts = time.strftime('%A %d %B %Y %I %M %S %p')
            cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            return frame

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:

            # frame = event_handle.detect_smile(frame)
            # frame = event_handle.detect_fall(frame)
            # frame = event_handle.detect_invasion(frame,self.first_frame())

            ts = time.strftime('%A %d %B %Y %I %M %S %p')
            cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            ret, jpeg = cv2.imencode('.jpg', frame)

            return jpeg.tobytes()

        else:
            return None

    def first_frame(self):
        n = 1
        while n < 30:
            success, image = self.cap.read()
            n += 1
        return image

    def release_camera(self):
        self.cap.release()

