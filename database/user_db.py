import datetime
import json
import pymysql
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()


# select
def getUsers():
    sql = "select * from sys_user"
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['ID'] = int(float(em[0]))
        data['ORG_ID'] = int(float(em[1]))
        data['CLIENT_ID'] = int(float(em[2]))
        data['UserName'] = str(em[3])
        data['Password'] = str(em[4])
        data['REAL_NAME'] = str(em[5])
        data['SEX'] = str(em[6])
        data['EMAIL'] = str(em[7])
        data['PHONE'] = str(em[8])
        data['MOBILE'] = str(em[9])
        data['DESCRIPTION'] = str(em[10])
        data['ISACTIVE'] = str(em[11])
        data['CREATED'] = str(em[12])
        data['CREATEBY'] = int(float(em[13]))
        data['UPDATED'] = str(em[14])
        data['UPDATEBY'] = int(float(em[15]))
        data['REMOVE'] = str(em[16])
        data['DATAFILTER'] = str(em[17])
        data['theme'] = str(em[18])
        data['defaultpage'] = str(em[19])
        data['logoimage'] = str(em[20])
        data['qqopenid'] = str(em[21])
        data['appversion'] = str(em[22])
        data['jsonauth'] = str(em[23])
        jsondata.append(data)
    jsondatas = json.dumps(jsondata, ensure_ascii=False)
    return jsondatas

def getUserID(name):
    sql = "select ID from sys_user where UserName='" + name + "'"
    conn.execute(sql)
    result = conn.fetchall()
    if result:
        (id,) = result[0]
        return id
    return 0

def userlogin(name,password):
    sql = "select Password from sys_user where UserName='" + name + "'"
    print(sql)
    conn.execute(sql)
    result = conn.fetchall()
    if result:
        (password1,) = result[0]
        # print(password1)
        if password == password1:
            return True
    return False

#获得密码
def getpassword(email):
    sql = "select Password from sys_user where EMAIL='" + email + "'"
    conn.execute(sql)
    result = conn.fetchall()
    if result:
        (password1,) = result[0]
        return password1
    return ""

# update
def updateUser(id, name):
    sql = "update sys_user set UserName='" + name + "' where id=" + str(id)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


def updateU(ID,ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
            DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
            theme, defaultpage, logoimage, qqopenid, appversion, jsonauth):
    deleteUserById(ID)
    addUser_with_ID(ID,ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
            DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
            theme, defaultpage, logoimage, qqopenid, appversion, jsonauth)


# add 含ID
def addUser_with_ID(ID,ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
            DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
            theme, defaultpage, logoimage, qqopenid, appversion, jsonauth):
    sql = "insert into sys_user(ID,ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME,SEX, " \
          "EMAIL,PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE,DATAFILTER," \
          "theme,defaultpage,logoimage,qqopenid,appversion,jsonauth) " \
          "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (ID,0, 0, "'" + UserName + "'", "'" + Password + "'", "'" + REAL_NAME + "'", "'" + SEX + "'",
           "'" + EMAIL + "'", "'" + PHONE + "'", "'" + MOBILE + "'", "'" + DESCRIPTION + "'", "'" + ISACTIVE + "'",
           "'" + CREATED + "'"
           , CREATEBY, "'" + UPDATED + "'", UPDATEBY, "'" + REMOVE + "'", "'" + DATAFILTER + "'", "'" + theme + "'",
           "'" + defaultpage + "'"
           , "'" + logoimage + "'", "'" + qqopenid + "'", "'" + appversion + "'", "'" + jsonauth + "'")
    print(sql)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

# add
def addUser(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME, SEX, EMAIL, PHONE, MOBILE,
            DESCRIPTION, ISACTIVE, CREATED, CREATEBY, UPDATED, UPDATEBY, REMOVE, DATAFILTER,
            theme, defaultpage, logoimage, qqopenid, appversion, jsonauth):
    sql = "insert into sys_user(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME,SEX, " \
          "EMAIL,PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE,DATAFILTER," \
          "theme,defaultpage,logoimage,qqopenid,appversion,jsonauth) " \
          "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (0, 0, "'" + UserName + "'", "'" + Password + "'", "'" + REAL_NAME + "'", "'" + SEX + "'",
           "'" + EMAIL + "'", "'" + PHONE + "'", "'" + MOBILE + "'", "'" + DESCRIPTION + "'", "'" + ISACTIVE + "'",
           "'" + CREATED + "'"
           , CREATEBY, "'" + UPDATED + "'", UPDATEBY, "'" + REMOVE + "'", "'" + DATAFILTER + "'", "'" + theme + "'",
           "'" + defaultpage + "'"
           , "'" + logoimage + "'", "'" + qqopenid + "'", "'" + appversion + "'", "'" + jsonauth + "'")
    print(sql)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


# delete
def deleteUserById(id):
    sql = "delete from sys_user where id=" + str(id)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

# delete
def deleteUserByName(name):
    sql = "delete from sys_user where UserName='" + name+"'"
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
# addUser(0,0,"sys","123456","system","boy","email@123","112234","123456","good","yes",now,12,now,12,'n',"null",
#         "theme","defaultpage","loginimage","qqopenid","appversion","json")
# deleteVolunteer(63)
# updateVolunteer(1,"HHH")
#print(userlogin("sys","123456"))
#print(getUserID('sys'))
