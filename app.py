import json
from flask import Flask, render_template, Response, request, redirect, url_for
from database import employee_db, event_db, oldperson_db, user_db, volunteer_db
from video import image_stream
import video.views as vv

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index_video.html')


@app.route('/test')
def img_stream():
    img_path = 'static/images/bg1.jpg'
    img_stream = image_stream.image_stream(img_path)

    return render_template('test.html', img_stream=img_stream)


# 主界面
@app.route('/index')
def tempindex():
    return render_template('index.html')


# 视频流
@app.route('/video_viewer')
def video_viewer():
    return Response(vv.video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


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

        print(user_db.getpassword(email))#根据email打印密码
        return " "


@app.route('/old-people', methods=['GET', 'POST'])
def oldpeople():
    if request.method == 'GET':
        return render_template('old-people.html')
    if request.method == 'POST':
        return oldperson_db.getOldpersons()   #获得oldperson信息

@app.route('/oldpeople-detail', methods=['GET', 'POST'])
def detail_old():
    if request.method == 'GET':
        return render_template('oldpeople-detail.html')

@app.route('/newoldpeople', methods=['GET', 'POST'])
def newoldpeople():
    if request.method == 'GET':
        return render_template('newoldpeople.html')  #添加老人信息
    if request.method == 'POST':    #提交新增老人信息
        recv_data = request.get_data()
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
        ISACTIVE = jsondata.get("ISACTIVE")
        CREATED = jsondata.get("CREATED")
        CREATEBY = jsondata.get("CREATEBY")
        UPDATED = jsondata.get("UPDATED")
        UPDATEBY = jsondata.get("UPDATEBY")
        REMOVE = jsondata.get("REMOVE")

        # oldperson_db.addOld(ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,
        #         profile_photo,room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat
        #    ,secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,
        #    health_state,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)
        return "success"


@app.route('/deleteold',methods=['GET','POST'])
def delete_oldpeople():
    if request.method == 'POST':
        recv_data = request.get_data()
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
        ISACTIVE = jsondata.get("ISACTIVE")
        CREATED = jsondata.get("CREATED")
        CREATEBY = jsondata.get("CREATEBY")
        UPDATED = jsondata.get("UPDATED")
        UPDATEBY = jsondata.get("UPDATEBY")
        REMOVE = jsondata.get("REMOVE")

        oldperson_db.updateOld(id,ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, checkin_date, checkout_date,
           imgset_dir,profile_photo,room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
           secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,
           health_state,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)

        return "success"



@app.route('/updateold',methods=['GET','POST'])
def update_oldpeople():
    if request.method == 'POST':
        data = request.get_data()
        jdata = json.loads(data)
        name = jdata.get("username")
        print(name)
        oldperson_db.updateOld(name)
        return "success"

@app.route('/employee')
def employee():
    return employee_db.getEmployees()


@app.route('/event')
def event():
    return event_db.getEvents()


@app.route('/volunteer')
def volunteer():
    return volunteer_db.getVolunteers()


@app.route('/oldperson')
def oldperson():
    return oldperson_db.getOldpersons()#年龄
    #return oldperson_db.getOlds() #birthday


@app.route('/user')
def user():
    return user_db


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
