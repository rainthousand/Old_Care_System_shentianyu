# -*- coding: utf-8 -*-
'''
测试人脸识别模型

用法：
python testingfacerecognition.py
python testingfacerecognition.py --filename room_01.mp4
'''

# import the necessary packages
from oldcare.facial import FaceUtil
import imutils
import cv2
import time
import argparse
import math

# 传入参数
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=False, default='',
                help="")
args = vars(ap.parse_args())

# 全局变量
facial_recognition_model_path = 'models/face_recognition_hog.pickle'
input_video = args['filename']

old_name = '106'
work_name = '103'

def calculate_distance(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return math.sqrt(x*x+y*y)



# 初始化摄像头
if not input_video:
    vs = cv2.VideoCapture(0)
    time.sleep(2)
else:
    vs = cv2.VideoCapture(input_video)

# 初始化人脸识别模型
faceutil = FaceUtil(facial_recognition_model_path)

# 不断循环
while True:
    # grab the current frame
    (grabbed, frame) = vs.read()

    # if we are viewing a video and we did not grab a frame, then we
    # have reached the end of the video
    if input_video and not grabbed:
        break

    if not input_video:
        frame = cv2.flip(frame, 1)

    # resize the frame, convert it to grayscale, and then clone the
    # original frame so we can draw on it later in the program
    frame = imutils.resize(frame, width=600)

    face_location_list, names = faceutil.get_face_location_and_name(
        frame)

    interaction = False

    if work_name in names and old_name in names:
        interaction = True

    points = []

    point_size = 5
    point_color = (0, 0, 255)
    thickness = 4

    # loop over the face bounding boxes
    for ((left, top, right, bottom), name) in zip(
            face_location_list,
            names):
        # display label and bounding box rectangle on the output frame
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 0, 255), 2)


        if old_name == name or work_name == name:
            points.append((int((left+right)/2), int((top+bottom)/2)))

        if interaction:
            cv2.circle(frame, (int((left+right)/2), int((top-bottom)/2)), point_size, color=point_color, thickness=thickness)
            #print("interaction process")

    if interaction:
        distance = calculate_distance(points[0], points[1])

        if distance < 100:
            cv2.line(frame, points[0], points[1], color=point_color, thickness=thickness)
            cv2.putText(frame, 'distance %d cm' % distance, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # show our detected faces along with smiling/not smiling labels
    cv2.imshow("Face Recognition", frame)

    # Press 'ESC' for exiting video
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()

