import datetime
import json

import cv2

from database import event_db
from version.activity import testingvolunteeractivity
from version.face_api import face
from version.falldown.FallDownDetection import fallDetect2
from version.invasion.invasionDetection import invasionDetect
from version.smile.smileDetection import smileDetect
from version.stranger.testingstranger import get_new_stranger_frame

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
invasion_sign = 0

def event_to_json(event_type, event_date, event_location, event_desc, oldperson_id):
    data = {"event_type": event_type, "event_date": event_date, "event_location": event_location,
            "event_desc": event_desc, "oldperson_id": oldperson_id}
    jdata = json.dumps(data)
    return jdata


def detect_event(y):
    return y

def detect_smile(frame):
    smile_num = 0
    frame, sign = smileDetect(frame)
    if sign:
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        smile_num = smile_num + 1
        frames_save_path = "F:\\Pycharm_project\\care_sys\\image\\smile" + str(smile_num) + ".png"
        cv2.imwrite(frames_save_path, frame)
        event_db.addEvent(0,now,"location","smile",61)
    return frame

def detect_fall():
    # fall_num = 0
    # frame, sign = fallDetect2(frame)
    # if sign:
    #     fall_num = fall_num + 1
    #     frames_save_path = "F:\\Pycharm_project\\care_sys\\image\\fall" + str(fall_num) + ".png"
    #     cv2.imwrite(frames_save_path, frame)
    # cv2.imshow("fall",frame)
    return fallDetect2('F:\\Pycharm_project\\care_sys\\version\\falldown\\fall.mp4')

def detect_invasion(frame,first):
    global invasion_sign
    invasion_num = 0
    #first = VideoCamera.first_frame()
    frame, sign = invasionDetect(frame, first)
    if sign:
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        invasion_sign = 1
        invasion_num = invasion_num + 1
        frames_save_path = "F:\\Pycharm_project\\care_sys\\image\\invasion" + str(invasion_num) + ".png"
        cv2.imwrite(frames_save_path, frame)
        event_db.addEvent(4, now, "location", "stranger_invade", 0)

    return frame


def detect_face(frame):
    return face.get_new_frame(frame)


def detect_volun_activity(frame):
    return testingvolunteeractivity.get_new_activity_frame(frame)

def detect_stranger(frame):
   return get_new_stranger_frame(frame)
#print(event_to_json("da","dwad","dwad","dwad",12))
