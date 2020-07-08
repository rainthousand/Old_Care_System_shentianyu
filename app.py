import copy
import datetime
import json
import requests
import base64
import cv2
import numpy as np
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from flask import Flask, render_template, Response, request, redirect, url_for, abort, session
from version.collect import collectingfaces

from config import config_dict
from event_ws import event_handle
from database import employee_db, event_db, oldperson_db, user_db, volunteer_db, schedule_db
import video.image_stream as ims

config_class = config_dict['dev']
app = Flask(__name__)
app.config.from_object(config_class)
user_socket_list = []


@app.route('/video', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('video.html')


# #图片流
# @app.route('/test')
# def img_stream():
#     img_path = 'static/images/bg1.jpg'
#     img_stream = image_stream.image_stream(img_path)
#
#     return render_template('test.html', img_stream=img_stream)

# 主界面
@app.route('/index')
def tempindex():
    return render_template('index.html')


@app.route('/question')
def question():
    return render_template('question.html')


# 视频测试
@app.route('/videotest')
def video_test():
    return render_template('index_video.html')


@app.route('/video_viewer')
def video_viewer():
    return Response(collectingfaces.get_face_collect_frame("./image/faces/old_people", '302'), mimetype='multipart/x-mixed-replace; boundary=frame')
    # if not session.get("username"):
    #     return redirect(url_for("login"))


# 普通视频流
@app.route('/video_socket')
def video_socket():
    path_smile = "static\\images\\smile.jpg"
    path_invas = "static\\images\\invas.jpg"
    path_face = "static\\images\\face.jpg"
    path_volun_act = "static\\images\\volun_act.jpg"
    pathfall = "static\\images\\tempfall.jpg"
    pathfire = "static\\images\\tempfire.jpg"
    fall_video_path = 'version\\falldown\\fall_new.mp4'
    fire_video_path = "version\\fire\\fire_new.mp4"

    fall_k = 0
    fire_k = 0
    invas_k = 0
    first_frame = None

    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    if user_socket is None:
        abort(404)
    else:
        print("WebSocket Connected!!!")
        camera = cv2.VideoCapture(0)

        fall_vid = cv2.VideoCapture(fall_video_path)
        fall_fs = fall_vid.get(7)
        fire_vid = cv2.VideoCapture(fire_video_path)
        fire_fs = fire_vid.get(7)

        headers = {'Proxy-Connection': 'keep-alive'}

        while True:
            suc, fall = fall_vid.read()
            if suc:
                if fall_k == fall_fs - 1:  # 最后一帧
                    fall_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    fall_k = 0
                cv2.imwrite(pathfall, fall)
                user_socket.send("2$" + ims.image_stream(pathfall))
                fall_k += 1

            succc, fire = fire_vid.read()
            if succc:
                if fire_k == fire_fs - 1:
                    fire_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    fire_k = 0
                cv2.imwrite(pathfire, fire)
                user_socket.send("4$" + ims.image_stream(pathfire))
                fire_k += 1

            ret, frame = camera.read()

            # img = requests.get("http://127.0.0.1:6000/getvideo", stream=True, headers=headers)
            # print("content:::::::::::::::::::::::")
            # print(img.content)

            # img = base64.b64decode(img.content)
            # image_data = base64.b64decode(str(img))
            # image_data = np.fromstring(img, np.uint8)
            # frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # img_data = base64.b64decode(str(img.content))
            # imgData = base64.b64decode(img.content)
            # nparr = np.fromstring(imgData, np.uint8)
            # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # img_array = np.fromstring(img_data, np.uint8)  # 转换np序列
            # print(img_array)
            # frame = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式

            if frame is None:
                print("no frame")
            # print(frame)
            else:
                cv2.imshow("test", frame)
                frame_inv = copy.copy(frame)
                frame_s = copy.copy(frame)
                frame_face = copy.copy(frame)
                frame_vol_act = copy.copy(frame)
                frame_temp = copy.copy(frame)
                # 人脸检测
                frame_f = event_handle.detect_face(frame_face)
                cv2.imwrite(path_face, frame_f)
                user_socket.send("5$" + ims.image_stream(path_face))
                #义工活动
                frame_va = event_handle.detect_volun_activity(frame_vol_act)
                cv2.imwrite(path_volun_act, frame_va)
                user_socket.send("6$" + ims.image_stream(path_volun_act))
                # 入侵
                if invas_k % 10 == 0:
                    first_frame = frame_temp
                frame_invas = event_handle.detect_invasion(frame_inv, first_frame)
                invas_k += 1
                cv2.imwrite(path_invas, frame_invas)
                user_socket.send("3$" + ims.image_stream(path_invas))
                # 微笑
                frame_smile = event_handle.detect_smile(frame_s)
                cv2.imwrite(path_smile, frame_smile)
                user_socket.send("1$" + ims.image_stream(path_smile))


        #     key = cv2.waitKey(1) & 0xFF
        #     if key == ord('s'):
        #         break
        #     elif key == 27:
        #         break
        # cv2.destroyAllWindows()
        # camera.release()
    return "success"

    # if not session.get("username"):
    #     return redirect(url_for("login"))


# @app.route('/enter_face')
# def enter_face():
#     return Response(collectingfaces.get_face_collect_frame("./image/faces/old_people", '302'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/catch_face')
def catch_face():
    return render_template("catch_face.html")


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        recv_data = request.get_data()
        jsondata = json.loads(recv_data)
        # print(jsondata)
        user_name = jsondata.get("username")
        user_password = jsondata.get("password")
        print(user_name + user_password)
        print(user_db.userlogin(user_name, user_password))
        if user_db.userlogin(user_name, user_password):
            session["username"] = user_name
            return "success"
            # return render_template('index.html')
        return " "


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        jsondata = json.loads(recv_data)
        # print(jsondata)
        ORG_ID = 0
        CLIENT_ID = 0
        UserName = jsondata.get("UserName")
        Password = jsondata.get("Password")
        REAL_NAME = jsondata.get("REAL_NAME")
        SEX = jsondata.get("SEX")
        EMAIL = jsondata.get("EMAIL")
        PHONE = jsondata.get("PHONE")
        MOBILE = jsondata.get("PHONE")  # jsondata.get("MOBILE")
        DESCRIPTION = "new"  # jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"  # jsondata.get("ISACTIVE")
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = 0  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = 0  # jsondata.get("UPDATEBY")
        REMOVE = "no"  # jsondata.get("REMOVE")
        DATAFILTER = "new register"  # jsondata.get("DATAFILTER")
        theme = "theme"  # jsondata.get("theme")
        defaultpage = "defaultpage"  # jsondata.get("defaultpage")
        logoimage = "loginimage"  # jsondata.get("logoimage")
        qqopenid = "qqopenid"  # jsondata.get("qqopenid")
        appversion = "appversion"  # jsondata.get("appversion")
        jsonauth = "jsonquth"  # jsondata.get("jsonauth")
        print(UserName + Password)

        user_db.addUser(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
                        DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
                        theme, defaultpage, logoimage, qqopenid, appversion, jsonauth)

        return "success"


# 忘记密码
@app.route('/forget-password', methods=['GET', 'POST'])
def forgetpassword():
    if request.method == 'GET':
        return render_template('forgot-password.html')
    if request.method == 'POST':
        recv_data = request.get_data()
        jsondata = json.loads(recv_data)
        # print(jsondata)
        email = jsondata.get("EMAIL")
        print(email)

        print(user_db.getpassword(email))  # 根据email打印密码
        return " "

#日程表_________________________________________________________________________calender
@app.route('/calender', methods=['GET', 'POST'])
def calender():
    if request.method == 'GET':
        return render_template('calender.html')
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        name = jdata.get("username")
        print(name)
        returndata = schedule_db.getScheduleByUserName(name)
        return returndata

@app.route('/addschedule', methods=['GET', 'POST'])
def new_schedule():
    if request.method == 'POST':
        data = request.get_data()
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        sche_id = jdata.get("sche_id")
        sche_name = jdata.get("sche_name")
        start_date = jdata.get("start_date")
        end_date = jdata.get("end_date")
        sche_content = jdata.get("sche_content")
        username = jdata.get("username")
        color = jdata.get("color")

        schedule_db.addNewSchedule(sche_id,sche_name,start_date,end_date,sche_content,username,color)

        return "success"

@app.route('/deleteschedule', methods=['GET', 'POST'])
def delete_schedule():
    if request.method == 'POST':
        data = request.get_data()
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        sche_name = jdata.get("sche_name")
        username = jdata.get("username")

        schedule_db.deleteScheduleByName(sche_name,username)
        return "success"
#____________________________________________________________________________________calender

# _____________________________________________________________________________oldperson
@app.route('/old-people', methods=['GET', 'POST'])
def oldpeople():
    if request.method == 'GET':
        return render_template('old-people.html')
    if request.method == 'POST':
        return oldperson_db.getOldpersons()  # 获得oldperson信息


@app.route('/oldpeople-detail', methods=['GET', 'POST'])  # 查看按钮跳转
def detail_old():
    if request.method == 'GET':
        return render_template('oldpeople-detail.html')


# 添加
@app.route('/newoldpeople', methods=['GET', 'POST'])
def new_oldpeople():
    if request.method == 'GET':
        return render_template('newoldpeople.html')  # 添加老人信息
    if request.method == 'POST':  # 提交新增老人信息
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        if recv_data:
            print("data recv!!!")
        jsondata = json.loads(recv_data)
        print(jsondata)
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        username = jsondata.get("username")
        gender = jsondata.get("gender")
        phone = jsondata.get("phone")
        id_card = jsondata.get("id_card")
        birthday = jsondata.get("birthday")
        checkin_date = jsondata.get("checkin_date")
        checkout_date = jsondata.get("checkout_date")
        imgset_dir = jsondata.get("imgset_dir")
        profile_photo = jsondata.get("profile_photo")
        room_number = jsondata.get("room_number")
        firstguardian_name = jsondata.get("firstguardian_name")
        firstguardian_relationship = jsondata.get("firstguardian_relationship")
        firstguardian_phone = jsondata.get("firstguardian_phone")
        firstguardian_wechat = jsondata.get("firstguardian_wechat")
        secondguardian_name = jsondata.get("secondguardian_name")
        secondguardian_relationship = jsondata.get("secondguardian_relationship")
        secondguardian_phone = jsondata.get("secondguardian_phone")
        secondguardian_wechat = jsondata.get("secondguardian_wechat")
        health_state = jsondata.get("health_state")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'

        oldperson_db.addOld(ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, checkin_date, checkout_date,
                            imgset_dir,
                            profile_photo, room_number, firstguardian_name, firstguardian_relationship,
                            firstguardian_phone, firstguardian_wechat
                            , secondguardian_name, secondguardian_relationship, secondguardian_phone,
                            secondguardian_wechat,
                            health_state, DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE)
        return "success"


@app.route('/updateold', methods=['GET', 'POST'])
def update_oldpeople():
    if request.method == 'POST':
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        jsondata = json.loads(recv_data)
        print(jsondata)
        id = jsondata.get("ID")
        print(id)
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        username = jsondata.get("username")
        gender = jsondata.get("gender")
        phone = jsondata.get("phone")
        id_card = jsondata.get("id_card")
        birthday = jsondata.get("birthday")
        checkin_date = jsondata.get("checkin_date")
        checkout_date = jsondata.get("checkout_date")
        imgset_dir = jsondata.get("imgset_dir")
        profile_photo = jsondata.get("profile_photo")
        room_number = jsondata.get("room_number")
        firstguardian_name = jsondata.get("firstguardian_name")
        firstguardian_relationship = jsondata.get("firstguardian_relationship")
        firstguardian_phone = jsondata.get("firstguardian_phone")
        firstguardian_wechat = jsondata.get("firstguardian_wechat")
        secondguardian_name = jsondata.get("secondguardian_name")
        secondguardian_relationship = jsondata.get("secondguardian_relationship")
        secondguardian_phone = jsondata.get("secondguardian_phone")
        secondguardian_wechat = jsondata.get("secondguardian_wechat")
        health_state = jsondata.get("health_state")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'

        oldperson_db.updateOld(id, ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, checkin_date,
                               checkout_date,
                               imgset_dir, profile_photo, room_number, firstguardian_name, firstguardian_relationship,
                               firstguardian_phone, firstguardian_wechat,
                               secondguardian_name, secondguardian_relationship, secondguardian_phone,
                               secondguardian_wechat,
                               health_state, DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE)

        return "success"


@app.route('/deleteold', methods=['GET', 'POST'])
def delete_oldpeople():
    if request.method == 'POST':
        data = request.get_data()
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        name = jdata.get("username")
        print(name)
        oldperson_db.deleteOld_by_Name(name)
        return "success"


# _____________________________________________________________________________oldperson
# ————————————————————————————————————————————————————————————————————————————————————————————————————————————employee
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if request.method == 'GET':
        return render_template("employee.html")
    if request.method == 'POST':
        return employee_db.getEmployees()


@app.route('/employee-detail', methods=['GET', 'POST'])  # 查看按钮跳转
def detail_employ():
    if request.method == 'GET':
        return render_template('employee-detail.html')


# 添加
@app.route('/newemployee', methods=['GET', 'POST'])
def new_employee():
    if request.method == 'GET':
        return render_template('newemployee.html')  # 添加老人信息
    if request.method == 'POST':  # 提交新增老人信息
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        if recv_data:
            print("data recv!!!")
        jsondata = json.loads(recv_data)
        print(jsondata)
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        username = jsondata.get("username")
        gender = jsondata.get("gender")
        phone = jsondata.get("phone")
        id_card = jsondata.get("id_card")
        birthday = jsondata.get("birthday")
        hire_date = jsondata.get("hire_date")
        resign_date = jsondata.get("resign_date")
        imgset_dir = jsondata.get("imgset_dir")
        profile_photo = jsondata.get("profile_photo")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'

        employee_db.addEmployee(ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, hire_date, resign_date,
                                imgset_dir,
                                profile_photo, DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE)
        return "success"


@app.route('/updatemployee', methods=['GET', 'POST'])
def update_employee():
    if request.method == 'POST':
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        if recv_data:
            print("data recv!!!")
        jsondata = json.loads(recv_data)
        print(jsondata)
        id = jsondata.get("id")
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        username = jsondata.get("username")
        gender = jsondata.get("gender")
        phone = jsondata.get("phone")
        id_card = jsondata.get("id_card")
        birthday = jsondata.get("birthday")
        hire_date = jsondata.get("hire_date")
        resign_date = jsondata.get("resign_date")
        imgset_dir = jsondata.get("imgset_dir")
        profile_photo = jsondata.get("profile_photo")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'

        employee_db.updateEmp(id, ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, hire_date, resign_date,
                              imgset_dir,
                              profile_photo, DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE)

        return "success"


@app.route('/deletemployee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        data = request.get_data()
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        name = jdata.get("username")
        print(name)
        employee_db.deleteEmployeeByName(name)
        return "success"


# -------------------------------------------------------------------------------————————————————————————————————employee
# --————————————————————————————————————————————————————————————————————————————————-------------event
@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'GET':
        return render_template('event.html')
    if request.method == 'POST':
        return event_db.getEvents()


# websocket传event
@app.route('/event_ws')
def event_send():
    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    user_socket_list.append(user_socket)
    if user_socket is None:
        abort(404)
    else:
        jsondata = []
        data = {'id': 1, 'event_type': '2', 'event_date': '3', 'event_location': '2', 'event_desc': '3',
                'oldperson_id': 0}
        data['id'] = 6
        data['event_type'] = "1"
        data['event_date'] = "6-5"
        data['event_location'] = "kitchen"
        data['event_desc'] = "reallyGOOD"
        data['oldperson_id'] = "2"
        jsondata.append(data)
        jsondatas = json.dumps(data)
        # while True:
        # message = user_socket.receive()
        # print(message)
        for user in user_socket_list:
            try:
                user.send(jsondatas)
            except Exception as e:
                continue
                # user_socket_list.remove(user_socket)
    return " "


# _____________________________________________________________________________________________event

# ______________________________________________________________________________________volunteer
@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'GET':
        return render_template('volunteer.html')
    if request.method == 'POST':
        return volunteer_db.getVolunteers()


# 添加志愿者
@app.route('/newvolunteer', methods=['GET', 'POST'])
def add_volunteer():
    if request.method == 'GET':
        return render_template('newvolunteer.html')
    if request.method == 'POST':
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        if recv_data:
            print("data recv!!!")
        jsondata = json.loads(recv_data)
        print(jsondata)
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        name = jsondata.get("name")
        gender = jsondata.get("gender")
        phone = jsondata.get("phone")
        id_card = jsondata.get("id_card")
        birthday = jsondata.get("birthday")
        checkin_date = jsondata.get("checkin_date")
        checkout_date = jsondata.get("checkout_date")
        imgset_dir = jsondata.get("imgset_dir")
        profile_photo = jsondata.get("profile_photo")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'
        volunteer_db.addVolunteer(ORG_ID, CLIENT_ID, name, gender, phone, id_card, birthday, checkin_date,
                                  checkout_date, imgset_dir,
                                  profile_photo, DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE)
        return "success"


@app.route('/volunteer-detail')  # 查看详情
def volunteer_detail():
    return render_template("volunteer-detail.html")


# 更新志愿者
@app.route('/updatevolunteer', methods=['GET', 'POST'])
def update_volunteer():
    if request.method == 'GET':
        return render_template('')
    if request.method == 'POST':
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        if recv_data:
            print("data recv!!!")
        jsondata = json.loads(recv_data)
        print(jsondata)
        id = jsondata.get("id")
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        name = jsondata.get("name")
        gender = jsondata.get("gender")
        phone = jsondata.get("phone")
        id_card = jsondata.get("id_card")
        birthday = jsondata.get("birthday")
        checkin_date = jsondata.get("checkin_date")
        checkout_date = jsondata.get("checkout_date")
        imgset_dir = jsondata.get("imgset_dir")
        profile_photo = jsondata.get("profile_photo")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'

        volunteer_db.updateVol(id, ORG_ID, CLIENT_ID, name, gender, phone, id_card, birthday, checkin_date,
                               checkout_date, imgset_dir,
                               profile_photo, DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE)
        return "success"


# 删除志愿者
@app.route('/deletevolunteer', methods=['GET', 'POST'])
def delete_volunteer():
    if request.method == 'POST':
        data = request.get_data()
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        name = jdata.get("name")
        print(name)
        volunteer_db.deleteVolunteerByName(name)
        return "success"


# ______________________________________________________________________________________volunteer

@app.route('/oldperson')  # 查看json数据
def oldperson():
    return oldperson_db.getOldpersons()  # 年龄
    # return oldperson_db.getOlds() #birthday


# _________________________________________________________________________________________manager
@app.route('/user')  # 查看json数据
def user():
    return user_db.getUsers()


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'GET':
        return render_template("manager.html")
    if request.method == 'POST':
        return user_db.getUsers()


@app.route('/manager-detail')
def manager_detail():
    return render_template("manager-detail.html")


# 添加
@app.route('/newmanager', methods=['GET', 'POST'])
def newmanager():
    if request.method == 'GET':
        return render_template("newmanager.html")
    if request.method == 'POST':  #
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        if recv_data:
            print("data recv!!!")
        jsondata = json.loads(recv_data)
        print(jsondata)
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        UserName = jsondata.get("UserName")
        Password = jsondata.get("Password")
        REAL_NAME = jsondata.get("REAL_NAME")
        SEX = jsondata.get("SEX")
        EMAIL = jsondata.get("EMAIL")
        PHONE = jsondata.get("PHONE")
        MOBILE = jsondata.get("MOBILE")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'
        DATAFILTER = jsondata.get("DATAFILTER")
        theme = jsondata.get("theme")
        defaultpage = jsondata.get("defaultpage")
        logoimage = jsondata.get("logoimage")
        qqopenid = jsondata.get("qqopenid")
        appversion = jsondata.get("appversion")
        jsonauth = jsondata.get("jsonauth")

        user_db.addUser(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
                        DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
                        theme, defaultpage, logoimage, qqopenid, appversion, jsonauth)
        return "success"


@app.route('/updatemanager', methods=['GET', 'POST'])
def update_manager():
    if request.method == 'POST':
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        recv_data = request.get_data()
        jsondata = json.loads(recv_data)
        print(jsondata)
        ID = jsondata.get("ID")
        print(ID)
        ORG_ID = jsondata.get("ORG_ID")
        CLIENT_ID = jsondata.get("CLIENT_ID")
        UserName = jsondata.get("UserName")
        Password = jsondata.get("Password")
        REAL_NAME = jsondata.get("REAL_NAME")
        SEX = jsondata.get("SEX")
        EMAIL = jsondata.get("EMAIL")
        PHONE = jsondata.get("PHONE")
        MOBILE = jsondata.get("MOBILE")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = "有效"
        CREATED = now  # jsondata.get("CREATED")
        CREATEBY = user_db.getUserID(jsondata.get("CREATEBY"))  # jsondata.get("CREATEBY")
        UPDATED = now  # jsondata.get("UPDATED")
        UPDATEBY = user_db.getUserID(jsondata.get("CREATEBY"))
        REMOVE = 'n'
        DATAFILTER = jsondata.get("DATAFILTER")
        theme = jsondata.get("theme")
        defaultpage = jsondata.get("defaultpage")
        logoimage = jsondata.get("logoimage")
        qqopenid = jsondata.get("qqopenid")
        appversion = jsondata.get("appversion")
        jsonauth = jsondata.get("jsonauth")

        user_db.updateU(ID, ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
                        DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
                        theme, defaultpage, logoimage, qqopenid, appversion, jsonauth)

        return "success"


@app.route('/deletemanager', methods=['GET', 'POST'])
def delete_manager():
    if request.method == 'POST':
        data = request.get_data()
        if data:
            print("rec!!!!!")
        jdata = json.loads(data)
        name = jdata.get("UserName")
        print(name)
        user_db.deleteUserByName(name)
        return "success"


# ____________________________________________________________________________________________manager


if __name__ == '__main__':
    # app.run(host='0.0.0.0', threaded=True)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    if server:
        print('server start!!!!!!!!!')
    else:
        print("ERROR")
    server.serve_forever()
