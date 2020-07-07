import base64
import time

import cv2

path = "F:\\Pycharm_project\\care_sys\\static\images\\temp.jpg"


# 视频流
def image_stream(img_local_path):
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream.decode("utf8")


def cv_photo():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        cv2.imshow('jiankong', frame)
        # cv2.imwrite(path, frame)
        #image_stream(path)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            break
        elif key == 27:
            break
    cv2.destroyAllWindows()
    camera.release()


def fall_video_stream():
    video_path = 'F:\\Pycharm_project\\care_sys\\version\\falldown\\fall.mp4'
    cap = cv2.VideoCapture(video_path)
    fs = cap.get(7)
    k = 0
    # k = 0
    # while k < cap.get(7):
    #     success, frame = cap.read()
    #     if not success:
    #         break
    #     cv2.imshow("sda",frame)
    #     k = k + 1
    #
    #     if cv2.waitKey(33) == 27:
    #         break
    #
    # cv2.destroyAllWindows()


# def fall_frame(path):
#     cap = cv2.VideoCapture(path)
#     fs = cap.get(7)
#     k = 0
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         if k == fs - 1:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             k = 0
#         cv2.imshow("sda", frame)
#         k += 1
#         if cv2.waitKey(33) == 27:
#             break
#     cv2.destroyAllWindows()

#cv_photo()
#fall_video_stream()
