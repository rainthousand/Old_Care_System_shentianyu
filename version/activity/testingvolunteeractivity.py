# -*- coding: utf-8 -*-
'''
义工是否和老人有互动主程序

用法：
python testingvolunteeractivity.py
python testingvolunteeractivity.py --filename tests/desk_01.mp4
'''

from version.activity.faceutildlib import FaceUtil
from scipy.spatial import distance as dist
from PIL import Image, ImageDraw, ImageFont
import cv2
import time
import imutils
import numpy as np
import argparse
from database import event_db
from database import oldperson_db
from database import volunteer_db
from database import employee_db
import json

# 传入参数
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=False, default='',
                help="")
args = vars(ap.parse_args())

# 全局变量
pixel_per_metric = None
input_video = args['filename']
model_path = './version/models/face_recognition_hog.pickle'
people_info_path = './version/info/people_info.csv'
global_frame = None

# 全局常量
FACE_ACTUAL_WIDTH = 20  # 单位厘米   姑且认为所有人的脸都是相同大小
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
ACTUAL_DISTANCE_LIMIT = 100  # cm


# -----------------------------------------------------
# 得到 ID->姓名的map 、 ID->职位类型的map
# id_card_to_name, id_card_to_type = fileassistant.get_people_info(
#     people_info_path)

# 查询数据库构造两个字典 id->姓名 id->职位类型

# print(id_card_to_name)
# print(id_card_to_type)

old_persons = json.loads(oldperson_db.getOldpersons())
employees = json.loads(employee_db.getEmployees())
volunteers = json.loads(volunteer_db.getVolunteers())

id_card_to_type = {}
id_card_to_name = {}

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

print(id_card_to_name)
print(id_card_to_type)

# -----------------------------------------------------
# 不断循环

def get_activity_frame():
    # 初始化摄像头
    if not input_video:
        vs = cv2.VideoCapture(0)
        time.sleep(2)
    else:
        vs = cv2.VideoCapture(input_video)

    # 加载模型
    faceutil = FaceUtil(model_path)

    print('[INFO] 开始检测义工和老人是否有互动...')
    global global_frame
    counter = 0
    while True:
        counter += 1
        # grab the current frame
        (grabbed, frame) = vs.read()

        # if we are viewing a video and we did not grab a frame, then we
        # have reached the end of the video
        if input_video and not grabbed:
            break

        if not input_video:
            frame = cv2.flip(frame, 1)

        frame = imutils.resize(frame,
                               width=VIDEO_WIDTH,
                               height=VIDEO_HEIGHT)  # 压缩，加快识别速度

        face_location_list, names = faceutil.get_face_location_and_name(
            frame)

        people_type_list = list(set([id_card_to_type[i] for i in names]))

        volunteer_centroids = []
        old_people_centroids = []
        old_people_name = []

        # loop over the face bounding boxes
        for ((left, top, right, bottom), name) in zip(face_location_list,
                                                      names):  # 处理单个人

            person_type = id_card_to_type[name]
            # 将人脸框出来
            rectangle_color = (0, 0, 255)
            if person_type == 'old_people':
                rectangle_color = (0, 0, 128)
            elif person_type == 'employee':
                rectangle_color = (255, 0, 0)
            elif person_type == 'volunteer':
                rectangle_color = (0, 255, 0)
            else:
                pass
            cv2.rectangle(frame, (left, top), (right, bottom),
                          rectangle_color, 2)

            if 'volunteer' not in people_type_list:  # 如果无义工则跳出循环
                continue

            if person_type == 'volunteer':  # 如果检测到有义工存在
                # 获得义工位置
                volunteer_face_center = (int((right + left) / 2),
                                         int((top + bottom) / 2))
                volunteer_centroids.append(volunteer_face_center)

                cv2.circle(frame,
                           (volunteer_face_center[0],
                            volunteer_face_center[1]),
                           8, (255, 0, 0), -1)

            elif person_type == 'old_people':  # 如果没有发现义工
                old_people_face_center = (int((right + left) / 2),
                                          int((top + bottom) / 2))
                old_people_centroids.append(old_people_face_center)
                old_people_name.append(name)

                cv2.circle(frame,
                           (old_people_face_center[0],
                            old_people_face_center[1]),
                           4, (0, 255, 0), -1)
            else:
                pass

            # 把人名写上(同时处理中文显示问题)
            img_PIL = Image.fromarray(cv2.cvtColor(frame,
                                                   cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_PIL)
            final_label = id_card_to_name[name]
            draw.text((left, top - 30), final_label,
                      font=ImageFont.truetype('./NotoSansCJK-Black.ttc',
                                              40), fill=(255, 0, 0))  # linux
            # 转换回OpenCV格式
            frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)

        # 在义工和老人之间划线
        for i in volunteer_centroids:
            for j_index, j in enumerate(old_people_centroids):
                pixel_distance = dist.euclidean(i, j)
                face_pixel_width = sum([i[2] - i[0] for i in
                                        face_location_list]) / len(face_location_list)
                pixel_per_metric = face_pixel_width / FACE_ACTUAL_WIDTH
                actual_distance = pixel_distance / pixel_per_metric

                if actual_distance < ACTUAL_DISTANCE_LIMIT:
                    cv2.line(frame, (int(i[0]), int(i[1])),
                             (int(j[0]), int(j[1])), (255, 0, 255), 2)
                    label = 'distance: %dcm' % (actual_distance)
                    cv2.putText(frame, label, (frame.shape[1] - 150, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255), 2)

                    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(time.time()))
                    print('[EVENT] %s, 房间桌子, %s 正在与义工交互.'
                          % (current_time,
                             id_card_to_name[old_people_name[j_index]]))

                    cv2.imwrite('./version/supervision/activity/'+current_time+".jpg", frame)
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    event_db.addEvent('1', current_time, 'location', '义工交互', name)


        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        if grabbed:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes()
                   + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + global_frame + b'\r\n\r\n')

        # Press 'ESC' for exiting video

    # cleanup the camera and close any open windows
    vs.release()
    cv2.destroyAllWindows()