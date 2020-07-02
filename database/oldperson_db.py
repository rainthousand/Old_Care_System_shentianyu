import datetime
import json
import dateutil.parser as parser
import pymysql
from database import connect
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
now_year = parser.parse(now).year
print(now_year)
#select
def getOlds():
    sql = "select * from oldperson_info"
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['ID'] = int(float(em[0]))
        data['ORG_ID'] = str(em[1])
        data['CLIENT_ID'] = str(em[2])
        data['username'] = str(em[3])
        data['gender'] = str(em[4])
        data['phone'] = str(em[5])
        data['id_card'] = str(em[6])
        data['birthday'] = str(em[7])
        data['checkin_date'] = str(em[8])
        data['checkout_date'] = str(em[9])
        data['imgset_dir'] = str(em[10])
        data['profile_photo'] = str(em[11])
        data['room_number'] = str(em[12])
        data['firstguardian_name'] = str(em[13])
        data['firstguardian_relationship'] = str(em[14])
        data['firstguardian_phone'] = str(em[15])
        data['firstguardian_wechat'] = str(em[16])
        data['secondguardian_name'] = str(em[17])
        data['secondguardian_relationship'] = str(em[18])
        data['secondguardian_phone'] = str(em[19])
        data['secondguardian_wechat'] = str(em[20])
        data['health_state'] = str(em[21])
        data['DESCRIPTION'] = str(em[22])
        data['ISACTIVE'] = str(em[23])
        data['CREATED'] = str(em[24])
        data['CREATEBY'] = int(float(em[25]))
        data['UPDATED'] = str(em[26])
        data['UPDATEBY'] = int(float(em[27]))
        data['REMOVE'] = str(em[28])
        jsondata.append(data)
    jsondatas = json.dumps(jsondata, ensure_ascii=False)
    return jsondatas

#birthday计算年龄
def getOldpersons():
    sql = "select * from oldperson_info"
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['ID'] = int(float(em[0]))
        data['ORG_ID'] = str(em[1])
        data['CLIENT_ID'] = str(em[2])
        data['username'] = str(em[3])
        data['gender'] = str(em[4])
        data['phone'] = str(em[5])
        data['id_card'] = str(em[6])
        data['age'] = str(now_year-parser.parse(str(em[7])).year)
        data['birthday'] = str(em[7])
        data['checkin_date'] = str(em[8])
        data['checkout_date'] = str(em[9])
        data['imgset_dir'] = str(em[10])
        data['profile_photo'] = str(em[11])
        data['room_number'] = str(em[12])
        data['firstguardian_name'] = str(em[13])
        data['firstguardian_relationship'] = str(em[14])
        data['firstguardian_phone'] = str(em[15])
        data['firstguardian_wechat'] = str(em[16])
        data['secondguardian_name'] = str(em[17])
        data['secondguardian_relationship'] = str(em[18])
        data['secondguardian_phone'] = str(em[19])
        data['secondguardian_wechat'] = str(em[20])
        data['health_state'] = str(em[21])
        data['DESCRIPTION'] = str(em[22])
        data['ISACTIVE'] = str(em[23])
        data['CREATED'] = str(em[24])
        data['CREATEBY'] = int(float(em[25]))
        data['UPDATED'] = str(em[26])
        data['UPDATEBY'] = int(float(em[27]))
        data['REMOVE'] = str(em[28])
        jsondata.append(data)
    jsondatas = json.dumps(jsondata, ensure_ascii=False)
    return jsondatas

#update
def updateOld(id,ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, checkin_date, checkout_date,
           imgset_dir,profile_photo,room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
           secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,
           health_state,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    #sql = "update oldperson_info set username='" + name + "' where id="+str(id)
    deleteOld_by_ID(id)
    addOld(ORG_ID, CLIENT_ID, username, gender, phone, id_card, birthday, checkin_date, checkout_date,
           imgset_dir,profile_photo,room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat,
           secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,
           health_state,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)

#add
def addOld(ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir,
                profile_photo,room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat
           ,secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat,
           health_state,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE):
    sql = "insert into oldperson_info (ORG_ID, CLIENT_ID, username, gender, phone,id_card, birthday,checkin_date,checkout_date,imgset_dir," \
          "profile_photo,room_number,firstguardian_name,firstguardian_relationship,firstguardian_phone,firstguardian_wechat" \
          ",secondguardian_name,secondguardian_relationship,secondguardian_phone,secondguardian_wechat," \
          "health_state,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (0,0,"'" + username + "'", "'" + gender + "'","'" + phone + "'", "'" + id_card + "'",
           "'" + birthday + "'", "'" + checkin_date + "'", "'" + checkout_date + "'","'" + imgset_dir + "'"
           ,"'" + profile_photo + "'","'" +room_number + "'","'" + firstguardian_name + "'","'" + firstguardian_relationship + "'",
           "'" + firstguardian_phone + "'","'" + firstguardian_wechat + "'","'" + secondguardian_name + "'","'" + secondguardian_relationship + "'",
           "'" + secondguardian_phone + "'","'" + secondguardian_wechat + "'","'" + health_state + "'",
           "'" + DESCRIPTION + "'","'" + ISACTIVE + "'","'" + CREATED + "'"
           ,CREATEBY,"'" + UPDATED + "'",UPDATEBY,"'" + REMOVE + "'")
    print(sql)
    connect.executeSql(sql)

#delete
def deleteOld_by_ID(id):
    sql = "delete from oldperson_info where id=" + str(id)
    connect.executeSql(sql)

def deleteOld_by_Name(name):
    sql = "delete from oldperson_info where username='" + name+"'"
    connect.executeSql(sql)

#addOld(0,0,"Wang","M","1234567","123",now,now,now,"E://","D://","106","Wa","Son","1234560","15612",
 #      "Lili","daughter","654321","1234","healthy","everything is ok","yes",now,12,now,12,'n')
#deleteOld(63)
#updateOld(1,"HHH")