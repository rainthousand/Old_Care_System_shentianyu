import time

from video.camera import VideoCamera
from invasion.invasionDetection import invasionDetect
from falldown.FallDownDetection import fallDetect
from smile.smileDetection import smileDetect
import cv2

video_camera = None
global_frame = None
fall_num = 0
smile_num = 0
invasion_num = 0

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

def video_stream_Fall():
    global fall_num
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()
        frame, sign = fallDetect(frame)
        if sign:
            fall_num = fall_num+1
            frames_save_path = "E:\\SaveImage\\Fall\\" + fall_num + ".png"
            cv2.imwrite(frames_save_path, frame)


        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')


def video_stream_Smile():
    global video_camera
    global global_frame
    global smile_num



    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()
        frame, sign = smileDetect(frame)
        if sign:
            smile_num = smile_num+1
            frames_save_path = "E:\\SaveImage\\Fall\\" + smile_num + ".png"
            cv2.imwrite(frames_save_path, frame)

        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')

def video_stream_Invasion():
    global video_camera
    global global_frame
    global invasion_num

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()
        first = video_camera.first_frame()
        frame, sign = invasionDetect(frame, first)

        if sign:
            invasion_num = invasion_num+1
            frames_save_path = "E:\\SaveImage\\Fall\\" + invasion_num + ".png"
            cv2.imwrite(frames_save_path, frame)

        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')