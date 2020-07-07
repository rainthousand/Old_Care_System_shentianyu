import datetime
import json
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, render_template, Response, request, redirect, url_for, abort
from geventwebsocket.websocket import WebSocket
from vision.falldown.FallDownDetection import fallDetect2
from database import employee_db, event_db, oldperson_db, user_db, volunteer_db
from vision.fire.fireDetection import fireDetect
from video import image_stream
import video.views as vv

app = Flask(__name__)



@app.route('/video')
def index():
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

# 视频测试
@app.route('/videotest')
def video_test():
    return render_template('index_video.html')

# 视频流
# @app.route('/video_viewer')
# def video_viewer():
#     return Response(vv.video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/video_viewer2')
# def video_viewer2():
#     return Response(vv.video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer2')
def video_viewer2():
    return Response(fireDetect(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_viewer')
def video_viewer():
    return Response(fallDetect2("vision/falldown/fall3.mp4"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_viewer')
# def video_viewer():
#     return Response(get_face_collect_frame('./image/faces/old_people', '302'), mimetype='multipart/x-mixed-replace; boundary=frame')

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
            return "success"
            # return render_template('index.html')
        return " "


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
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
        MOBILE = jsondata.get("MOBILE")
        DESCRIPTION = jsondata.get("DESCRIPTION")
        ISACTIVE = jsondata.get("ISACTIVE")
        CREATED = jsondata.get("CREATED")
        CREATEBY = jsondata.get("CREATEBY")
        UPDATED = jsondata.get("UPDATED")
        UPDATEBY = jsondata.get("UPDATEBY")
        REMOVE = jsondata.get("REMOVE")
        DATAFILTER = jsondata.get("DATAFILTER")
        theme = jsondata.get("theme")
        defaultpage = jsondata.get("defaultpage")
        logoimage = jsondata.get("logoimage")
        qqopenid = jsondata.get("qqopenid")
        appversion = jsondata.get("appversion")
        jsonauth = jsondata.get("jsonauth")
        print(UserName + Password)

        user_db.addUser(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
                        DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
                        theme, defaultpage, logoimage, qqopenid, appversion, jsonauth)

        return " "


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


@app.route('/eventtest', methods=['GET', 'POST'])
def eventtest():
    if request.method == 'GET':
        return render_template('websockettest_2.html')


# websocket传event
@app.route('/event_ws')
def event_send():
    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    if user_socket:
        print("here")
        ws = request.environ['wsgi.websocket']
        if ws is None:
            abort(404)
        else:
            while True:
                if not ws.closed:
                    # message = ws.receive()
                    ws.send("success!!!")

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
    # print("132")
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    if server:
        print('server start!!!!!!!!!')
    else:
        print("BO")
    server.serve_forever()
