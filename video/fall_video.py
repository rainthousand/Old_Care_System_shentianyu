import cv2


def get_frame():
    video_capture = cv2.VideoCapture("version/falldown/fall.mp4")
    if video_capture:
        print("yes")
    # 读帧
    success, frame = video_capture.read()
    while success:
        cv2.imshow('windows', frame)  # 显示
        success, frame = video_capture.read()  # 获取下一帧

    video_capture.release()
