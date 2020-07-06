# -*- coding: utf-8 -*-
'''
图像采集程序-人脸检测
由于外部程序需要调用它，所以不能使用相对路径

用法：
python collectingfaces.py --id 106 --imagedir /home/reed/git-project/old_care_system/任务源代码/任务5.老人员工义工人脸图像采集/images

'''
import argparse
from version.activity.faceutildlib import FaceUtil
import version.collect.audioplayer as audioplayer
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import shutil
import time
from version.collect.trainingfacerecognition import training

# 全局参数
# audio_dir = '/home/reed/git-project/old_care_system/任务源代码/任务5.老人员工义工人脸图像采集/audios'
global_frame = None

def get_face_collect_frame(image_dir, id):
    audio_dir = '../../audios'

    # 控制参数
    error = 0
    start_time = None
    limit_time = 2  # 2 秒

    # 传入参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-ic", "--id", required=False,
                    help="")
    ap.add_argument("-id", "--imagedir", required=False,
                    help="")
    args = vars(ap.parse_args())

    action_list = ['blink', 'open_mouth', 'smile', 'rise_head', 'bow_head',
                   'look_left', 'look_right']
    action_map = {'blink': '请眨眼', 'open_mouth': '请张嘴',
                  'smile': '请笑一笑', 'rise_head': '请抬头',
                  'bow_head': '请低头', 'look_left': '请看左边',
                  'look_right': '请看右边'}
    # 设置摄像头
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    faceutil = FaceUtil()


    global global_frame

    counter = 0
    while True:

        counter += 1
        ret, image = cam.read()
        if counter <= 10:  # 放弃前10帧
            continue
        image = cv2.flip(image, 1)

        if error == 1:
            end_time = time.time()
            difference = end_time - start_time
            print(difference)
            if difference >= limit_time:
                error = 0

        face_location_list = faceutil.get_face_location(image)
        for (left, top, right, bottom) in face_location_list:
            cv2.rectangle(image, (left, top), (right, bottom),
                          (0, 0, 255), 2)

        if ret:
            global_frame = image
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', image)[1].tobytes()
                   + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + global_frame + b'\r\n\r\n')

        #cv2.imshow('Collecting Faces', image)  # show the image
        # Press 'ESC' for exiting video
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break

        face_count = len(face_location_list)
        if error == 0 and face_count == 0:  # 没有检测到人脸
            print('[WARNING] 没有检测到人脸')
            # audioplayer.play_audio(os.path.join(audio_dir,
            #                                    'no_face_detected.mp3'))

            error = 1
            start_time = time.time()
        elif error == 0 and face_count == 1:  # 可以开始采集图像了
            print('[INFO] 可以开始采集图像了')
            # audioplayer.play_audio(os.path.join(audio_dir,
            #                                    'start_image_capturing.mp3'))

            break
        elif error == 0 and face_count > 1:  # 检测到多张人脸
            print('[WARNING] 检测到多张人脸')
            # audioplayer.play_audio(os.path.join(audio_dir,
            #                                    'multi_faces_detected.mp3'))
            error = 1
            start_time = time.time()
        else:
            pass

    # 新建目录
    # if os.path.exists(os.path.join(args['imagedir'], args['id'])):
    #     shutil.rmtree(os.path.join(args['imagedir'], args['id']), True)
    # os.mkdir(os.path.join(args['imagedir'], args['id']))

    if os.path.exists(os.path.join(image_dir, id)):
        shutil.rmtree(os.path.join(image_dir, id), True)
    os.mkdir(os.path.join(image_dir, id))

    # 开始采集人脸
    for action in action_list:
        audioplayer.play_audio(os.path.join(audio_dir, action + '.mp3'))
        action_name = action_map[action]

        counter = 1
        for i in range(15):
            print('%s-%d' % (action_name, i))
            ret, img_OpenCV = cam.read()
            img_OpenCV = cv2.flip(img_OpenCV, 1)
            origin_img = img_OpenCV.copy()  # 保存时使用

            face_location_list = faceutil.get_face_location(img_OpenCV)
            for (left, top, right, bottom) in face_location_list:
                cv2.rectangle(img_OpenCV, (left, top),
                              (right, bottom), (0, 0, 255), 2)

            img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV,
                                                   cv2.COLOR_BGR2RGB))

            draw = ImageDraw.Draw(img_PIL)
            draw.text((int(image.shape[1] / 2), 30), action_name,
                      font=ImageFont.truetype('./NotoSansCJK-Black.ttc', 40),
                      fill=(255, 0, 0))  # linux

            # 转换回OpenCV格式
            img_OpenCV = cv2.cvtColor(np.asarray(img_PIL),
                                      cv2.COLOR_RGB2BGR)

            if ret:
                global_frame = image
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', img_OpenCV)[1].tobytes()
                       + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n'
                       + global_frame + b'\r\n\r\n')

            # cv2.imshow('Collecting Faces', img_OpenCV)  # show the image

            # image_name = os.path.join(args['imagedir'], args['id'],
            #                           action + '_' + str(counter) + '.jpg')

            image_name = os.path.join(image_dir, id,
                                      action + '_' + str(counter) + '.jpg')

            cv2.imwrite(image_name, origin_img)
            # Press 'ESC' for exiting video
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            counter += 1


        # Press 'ESC' for exiting video
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break

    # 结束
    print('[INFO] 采集完毕')
    #audioplayer.play_audio(os.path.join(audio_dir, 'end_capturing.mp3'))

    training()

    # 释放全部资源
    cam.release()
    cv2.destroyAllWindows()


