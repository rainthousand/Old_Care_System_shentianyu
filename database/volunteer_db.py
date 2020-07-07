import datetime
import json
import dateutil.parser as parser
import pymysql
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
now_year = parser.parse(now).year

#select
def getVolunteers():
    sql = "select * from volunteer_info"
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['id'] = int(float(em[0]))
        data['ORG_ID'] = str(em[1])
        data['CLIENT_ID'] = str(em[2])
        data['name'] = str(em[3])
        data['gender'] = str(em[4])
        data['phone'] = str(em[5])
        data['id_card'] = str(em[6])
        data['birthday'] = str(em[7])
        data['age'] = str(now_year - parser.parse(str(em[7])).year)
        data['checkin_date'] = str(em[8])
        data['checkout_date'] = str(em[9])
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
def updateVolunteer(id,name):
    sql = "update volunteer_info set name='" + name + "' where id="+str(id)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def updateVol(id,ORG_ID, CLIENT_ID, name, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    deleteVolunteerByID(id)
    addVolunteer_With_ID(id,ORG_ID, CLIENT_ID, name, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)

def addVolunteer_With_ID(id,ORG_ID, CLIENT_ID, name, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    sql = "insert into volunteer_info" \
          "(id,ORG_ID, CLIENT_ID, name, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (id,0, 0, "'" + name + "'", "'" + gender + "'", "'" + phone + "'", "'" + id_card + "'",
           "'" + birthday + "'", "'" + checkin_date + "'", "'" + checkout_date + "'", "'" + imgset_dir + "'"
           , "'" + profile_photo + "'", "'" + DESCRIPTION + "'", "'" + ISACTIVE + "'", "'" + CREATED + "'"
           , CREATEBY, "'" + UPDATED + "'", UPDATEBY, "'" + REMOVE + "'")
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
def addVolunteer(ORG_ID, CLIENT_ID, name, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,
                profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    sql = "insert into volunteer_info" \
          "(ORG_ID, CLIENT_ID, name, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,profile_photo,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (0,0,"'" + name + "'", "'" + gender + "'","'" + phone + "'", "'" + id_card + "'",
           "'" + birthday + "'", "'" + checkin_date + "'", "'" + checkout_date + "'","'" + imgset_dir + "'"
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
def deleteVolunteerByID(id):
    sql = "delete from volunteer_info where id=" + str(id)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

#delete
def deleteVolunteerByName(name):
    sql = "delete from volunteer_info where name='" + name+"'"
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
#addVolunteer(0,0,"Old Wang","M","1234567","123",now,now,now,"E://","D://","good","yes",now,12,now,12,'n')
#deleteVolunteer(63)
#updateVolunteer(1,"HHH")