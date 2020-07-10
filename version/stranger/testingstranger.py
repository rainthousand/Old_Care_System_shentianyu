# 导入包
import imutils

from version.activity.faceutildlib import FaceUtil
import cv2
import time
from database import event_db
from database import oldperson_db
from database import volunteer_db
from database import employee_db
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np

model_path = './version/models/face_recognition_hog.pickle'
global_frame = None

# 全局常量
FACE_ACTUAL_WIDTH = 20  # 单位厘米   姑且认为所有人的脸都是相同大小
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
ACTUAL_DISTANCE_LIMIT = 100  # cm


def query_database():
    id_card_to_type = {}
    id_card_to_name = {}

    old_persons = json.loads(oldperson_db.getOldpersons())
    employees = json.loads(employee_db.getEmployees())
    volunteers = json.loads(volunteer_db.getVolunteers())

    for old_person in old_persons:
        id_card_to_name[str(old_person.get('ID'))] = old_person.get('username')
        id_card_to_type[str(old_person.get('ID'))] = 'old_people'

    for employee in employees:
        id_card_to_name[str(employee.get('id'))] = employee.get('username')
        id_card_to_type[str(employee.get('id'))] = 'employee'

    for volunteer in volunteers:
        id_card_to_name[str(volunteer.get('id'))] = volunteer.get('username')
        id_card_to_type[str(volunteer.get('id'))] = 'volunteer'

    id_card_to_name['Unknown'] = '陌生人'
    id_card_to_type['Unknown'] = ''

    return id_card_to_type, id_card_to_name


strangers_timing = 0  # 计时开始
strangers_start_time = 0  # 开始时间
strangers_limit_time = 2


def get_new_stranger_frame(frame):
    global strangers_timing
    global strangers_start_time

    id_card_to_type, id_card_to_name = query_database()

    img = cv2.flip(frame, 1)
    face_util = FaceUtil(model_path)
    img = imutils.resize(img, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
    face_location_list, names = face_util.get_face_location_and_name(img)

    for ((left, top, right, bottom), name) in zip(face_location_list,
                                                  names):  # 处理单个人

        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # cv2.putText(img, id_card_to_name[name], (left, top - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        img_PIL = Image.fromarray(cv2.cvtColor(img,
                                               cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_PIL)
        final_label = id_card_to_name[name]
        draw.text((left, top - 30), final_label,
                  font=ImageFont.truetype('./NotoSansCJK-Black.ttc',
                                          20), fill=(255, 0, 0))  # linux

        img = cv2.cvtColor(np.asarray(img_PIL),
                                  cv2.COLOR_RGB2BGR)

        if 'Unknown' in names:  # alert
            if strangers_timing == 0:  # just start timing
                strangers_timing = 1
                strangers_start_time = time.time()
            else:  # already started timing
                strangers_end_time = time.time()
                difference = strangers_end_time - strangers_start_time

                current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(time.time()))

                if difference < strangers_limit_time:
                    print('[INFO] %s, 房间, 陌生人仅出现 %.1f 秒. 忽略.' % (current_time, difference))
                else:  # strangers appear
                    event_desc = '陌生人出现!!!'
                    event_location = '房间'
                    print('[EVENT] %s, 房间, 陌生人出现!!!' % (current_time))
                    cv2.imwrite('./version/supervision/stranger/' + current_time + 'stranger' + '.jpg',
                                img)  # snapshot

                    event_db.addEvent('2', current_time, event_desc, event_location, name)
        else:  # everything is ok
            strangers_timing = 0

        if name == 'Unknown':
            # 开始陌生人追踪
            unknown_face_center = (int((right + left) / 2),
                                   int((top + bottom) / 2))

            cv2.circle(img, (unknown_face_center[0],
                               unknown_face_center[1]), 4, (0, 255, 0), -1)
    return img
