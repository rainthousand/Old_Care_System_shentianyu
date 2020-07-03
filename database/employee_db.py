import datetime
import json
import pymysql
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()
#select
def getEmployees():
    sql = "select * from employee_info"
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['id'] = int(float(em[0]))
        data['ORG_ID'] = str(em[1])
        data['CLIENT_ID'] = str(em[2])
        data['username'] = str(em[3])
        data['gender'] = str(em[4])
        data['phone'] = str(em[5])
        data['id_card'] = str(em[6])
        data['birthday'] = str(em[7])
        data['hire_date'] = str(em[8])
        data['resign_date'] = str(em[9])
        data['imgset_dir'] = str(em[10])
        data['profile_photo'] = str(em[11])
        data['DESCRIPTION'] = str(em[12])
        data['ISACTIVE'] = str(em[13])
        data['CREATED'] = str(em[14])
        data['CREATEBY'] = int(float(em[15]))
        data['UPDATED'] = str(em[16])
        data['UPDATEBY'] = int(float(em[17]))
        data['REMOVE'] = str(em[18])
        jsondata.append(data)
    jsondatas = json.dumps(jsondata, ensure_ascii=False)
    return jsondatas

#update
def updateEmployee(id,name):
    sql = "update employee_info set username='" + name + "' where id="+str(id)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def updateEmp(id,ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,hire_date,resign_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    deleteEmployeeByID(id)
    addEmployee_With_ID(id,ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,hire_date,resign_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)

def addEmployee_With_ID(id,ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,hire_date,resign_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    sql = "insert into employee_info" \
          "(id,ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,hire_date,resign_date,imgset_dir,profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (id,0,0,"'" + username + "'", "'" + gender + "'","'" + phone + "'", "'" + id_card + "'",
           "'" + birthday + "'", "'" + hire_date + "'", "'" + resign_date + "'","'" + imgset_dir + "'"
           ,"'" + profile_photo + "'","'" + DESCRIPTION + "'","'" + ISACTIVE + "'","'" + CREATED + "'"
           ,CREATEBY,"'" + UPDATED + "'",UPDATEBY,"'" + REMOVE + "'")
    print(sql)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


#add
def addEmployee(ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,hire_date,resign_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    sql = "insert into employee_info" \
          "(ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,hire_date,resign_date,imgset_dir,profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (0,0,"'" + username + "'", "'" + gender + "'","'" + phone + "'", "'" + id_card + "'",
           "'" + birthday + "'", "'" + hire_date + "'", "'" + resign_date + "'","'" + imgset_dir + "'"
           ,"'" + profile_photo + "'","'" + DESCRIPTION + "'","'" + ISACTIVE + "'","'" + CREATED + "'"
           ,CREATEBY,"'" + UPDATED + "'",UPDATEBY,"'" + REMOVE + "'")
    print(sql)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

#delete
def deleteEmployeeByID(id):
    sql = "delete from employee_info where id=" + str(id)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def deleteEmployeeByName(name):
    sql = "delete from employee_info where username='" + name+"'"
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
#addEmployee(1,1,"Old Wang","M","1234567","123",now,now,now,"E://","D://","good","yes",now,12,now,12,'n')
#deleteEmployee(63)
#updateEmployee(1,"HHH")