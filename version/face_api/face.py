import threading

import requests
from json import JSONDecoder
import cv2
import json
from version.activity.faceutildlib import FaceUtil
from database import event_db
from database import oldperson_db
import time


url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = '11Gew209e-E8vcwqsqjsf8MCmV7BbV2-'
secret = 'b6i0QAOIDLFmCw3fSAF5OGlmY-9cz7SA'

model_path = './version/models/face_recognition_hog.pickle'


# 请求face++api 并返回结果转成json
def face_detect_dict(img_content):
    image_data = cv2.imencode(".jpg", img_content)[1].tobytes()
    file = {'image_file': image_data}
    data = {"api_key": key, "api_secret": secret, "return_attributes": "gender,age,smiling,beauty,emotion"}
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    r = requests.post(url, data=data, files=file, headers=headers)
    try:
        r.raise_for_status()
        req_con = r.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        # 对其解码成字典格式
        return req_dict
    except Exception as e:
        print("请求API出错")
        print(e.__str__())
        return None


def get_emotion(req_dict):
    if req_dict is not None:
        if 'error_message' in req_dict.keys():
            return None
        face_number = req_dict.get('face_num')

        if face_number == 0:
            return None
        else:
            attributes = req_dict.get('faces')[0].get('attributes')
            emotion_dict = attributes.get('emotion')
            emotion_result = max(emotion_dict, key=emotion_dict.get)
            return emotion_result
    else:
        return None


def get_information(req_dict):
    information = []
    if 'error_message' in req_dict.keys():
        return None
    face_number = req_dict.get('face_num')

    if face_number == 0:
        return None
    else:
        faces = req_dict.get('faces')
        for face in faces:
            attributes = face.get('attributes')
            emotion_dict = attributes.get('emotion')
            emotion_result = max(emotion_dict, key=emotion_dict.get)
            face_rectangle = face.get('face_rectangle')
            top = face_rectangle.get('top')
            left = face_rectangle.get('left')
            width = face_rectangle.get('width')
            height = face_rectangle.get('height')
            information.append((emotion_result, top, left, width, height))
        return information


def get_rectangle(req_dict):
    if 'error_message' in req_dict.keys():
        return None
    face_number = req_dict.get('face_num')

    if face_number == 0:
        return None
    else:
        face_rectangle = req_dict.get('faces')[0].get('face_rectangle')
        top = face_rectangle.get('top')
        left = face_rectangle.get('left')
        width = face_rectangle.get('width')
        height = face_rectangle.get('height')
        return top, left, width, height


global_frame = None

faceutil = FaceUtil(model_path)


def press_esc():
    pass


def get_new_frame(frame):

    img = cv2.flip(frame, 1)

    old_persons = []

    for old in json.loads(oldperson_db.getOldpersons()):
        old_persons.append(str(old.get('ID')))

    face_location_list, names = faceutil.get_face_location_and_name(img)

    for ((left, top, right, bottom), name) in zip(face_location_list, names):
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0))
        cv2.putText(img, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        if name in old_persons:
            expression_image = img[top:bottom, left:right]
            req_dict = face_detect_dict(expression_image)
            emotion = get_emotion(req_dict)

            cv2.putText(img, emotion, (left + 100, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

            if emotion == 'happiness':
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                cv2.imwrite('./version/supervision/emotion/' +
                            current_time + get_emotion(req_dict) + '.jpg', img)

                # 写入数据库，记录老人微笑
                event_db.addEvent('0', current_time, 'location', name + ' ' + emotion, name)

    return img


def get_frame():
    global global_frame
    cap = cv2.VideoCapture(0)
    # cap.set(0, 160)  # set Width (the first parameter is property_id)
    # cap.set(1, 120)  # set Height
    while True:  # 拍100张图片就结束
        ret, img = cap.read()
        # 人脸检测不依赖色彩，所以先把人脸图像转成灰度图像
        img = cv2.flip(img, 1)

        old_persons = []

        for old in json.loads(oldperson_db.getOldpersons()):
            old_persons.append(str(old.get('ID')))

        face_location_list, names = faceutil.get_face_location_and_name(img)

        for ((left, top, right, bottom), name) in zip(face_location_list, names):
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0))
            cv2.putText(img, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

            if name in old_persons:
                expression_image = img[top:bottom, left:right]
                req_dict = face_detect_dict(expression_image)
                emotion = get_emotion(req_dict)

                cv2.putText(img, emotion, (left + 100, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                if emotion == 'happiness':
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    cv2.imwrite('./version/supervision/emotion/' +
                                current_time + get_emotion(req_dict) + '.jpg', img)

                    # 写入数据库，记录老人微笑
                    event_db.addEvent('0', current_time, 'location', name + ' ' + emotion, name)

        # Press 'ESC' for exiting video
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break

        if ret:
            global_frame = img
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', img)[1].tobytes()
                   + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + global_frame + b'\r\n\r\n')

    # 释放全部资源
    cap.release()
    cv2.destroyAllWindows()
