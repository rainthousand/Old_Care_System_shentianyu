import base64
import time

import cv2

from video.camera import VideoCamera

video_camera = None
global_frame = None

# 获取视频流
def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')


def close_camera():
    global video_camera
    if video_camera:
        video_camera.release_camera()


def open_camera():
    global video_camera
    video_camera = VideoCamera()


def fall_video_stream():
    video_path = 'F:\\Pycharm_project\\care_sys\\version\\falldown\\fall.mp4'
    vid = cv2.VideoCapture(video_path)
    while True:
        ret, frame = vid.read()
        time.sleep(0.1)
        if ret:
            ret,image = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n')
        else:
            break