import requests
from json import JSONDecoder
import cv2
import time
import threading
import queue

url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = '11Gew209e-E8vcwqsqjsf8MCmV7BbV2-'
secret = 'b6i0QAOIDLFmCw3fSAF5OGlmY-9cz7SA'

maxThreads = 50

threadmax = threading.BoundedSemaphore(20)


# 请求face++api 并返回结果转成json
def face_detect_dict(img):
    image = cv2.imencode(".jpg", img)[1].tobytes()
    threadmax.acquire()
    # file = {'image_file': open(image_path, 'rb')}
    file = {'image_file': image}
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
        if not get_information(req_dict):
            gender, age, emotion, rectangle = get_information(req_dict)
            top = rectangle.get('top')
            left = rectangle.get('left')
            width = rectangle.get('width')
            height = rectangle.get('height')
            cv2.rectangle(img, (left, top), (width, height),
                          (0, 0, 255), 2)
        threadmax.release()
        return req_dict
    except Exception as e:
        print("请求API出错")
        print(e.__str__())


def get_information(req_dict):
    face_num = req_dict.get('face_num')
    print(req_dict)
    if face_num > 0:
        attributes = req_dict.get('faces')[0].get('attributes')
        gender = attributes.get('gender').get('value')
        age = attributes.get('age').get('value')
        emotion = attributes.get('emotion')
        emotion = max(emotion, key=emotion.get)
        rectangle = attributes.get('face_rectangle')
        return gender, age, emotion, rectangle
    return None


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(0, 320)  # set Width (the first parameter is property_id)
    cap.set(1, 240)  # set Height
    time.sleep(2)

    while True:  # 拍100张图片就结束
        ret, img = cap.read()
        # 人脸检测不依赖色彩，所以先把人脸图像转成灰度图像

        print(get_information(face_detect_dict(img)))

        # Press 'ESC' for exiting video
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break

        cv2.imshow("face expression", img)

    cap.release()
    cv2.destroyAllWindows()
