import os
from playsound import playsound
import cv2

from version.collect import collectingfaces, audioplayer

# collectface = collectingfaces.get_face_collect_frame("./image/faces/old_people", '302')
# for face in collectface:
#     cv2.imshow("face",face)

# os.system("F:\\Pycharm_project\\care_sys\\version\\audios\\blink.mp3")  #使用系统自带的播放器
# playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\blink.mp3")
from version.collect.trainingfacerecognition import training

#training()