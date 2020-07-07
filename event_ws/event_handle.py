import datetime
import json

import cv2

from database import event_db
from vision.falldown.FallDownDetection import fallDetect
from vision.invasion.invasionDetection import invasionDetect
from vision.smile.smileDetection import smileDetect

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")


def event_msg(jsondata):
    event_type = jsondata.get("event_type")
    event_date = jsondata.get("event_date")
    event_location = jsondata.get("event_location")
    event_desc = jsondata.get("event_desc")
    oldperson_id = jsondata.get("oldperson_id")
    event_db.addEvent(event_type, event_date, event_location, event_desc, oldperson_id)


def event_to_json(event_type, event_date, event_location, event_desc, oldperson_id):
    data = {'event_type': event_type, 'event_date': event_date, 'event_location': event_location,
            'event_desc': event_desc, 'oldperson_id': oldperson_id}
    jdata = json.dumps(data)
    return jdata


def detect_event(y):
    return y

def detect_smile(frame):
    smile_num = 0
    frame, sign = smileDetect(frame)
    if sign:
        smile_num = smile_num + 1
        frames_save_path = "F:\\Pycharm_project\\care_sys\\image\\smile" + str(smile_num) + ".png"
        cv2.imwrite(frames_save_path, frame)

    return frame

def detect_fall(frame):
    fall_num = 0
    frame, sign, j = fallDetect(frame)
    if sign:
        fall_num = fall_num + 1
        frames_save_path = "F:\\Pycharm_project\\care_sys\\image\\fall" + str(fall_num) + ".png"
        cv2.imwrite(frames_save_path, frame)
    cv2.imshow("fall",frame)
    return frame

def detect_invasion(frame,first):
    invasion_num = 0
    #first = VideoCamera.first_frame()
    frame, sign = invasionDetect(frame, first)

    if sign:
        invasion_num = invasion_num + 1
        frames_save_path = "F:\\Pycharm_project\\care_sys\\image\\invasion" + str(invasion_num) + ".png"
        cv2.imwrite(frames_save_path, frame)

    return frame

# print(event_to_json("da","dwad","dwad","dwad",12))
