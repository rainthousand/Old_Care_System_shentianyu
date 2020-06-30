import datetime
import json
import pymysql
import connect
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()
#select
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

#update
def updateUser(id,name):
    sql = "update sys_user set UserName='" + name + "' where id="+str(id)

    connect.executeSql(sql)

#add
def addUser(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME,SEX,EMAIL,PHONE,MOBILE,
                DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE,DATAFILTER,
            theme,defaultpage,logoimage,qqopenid,appversion,jsonauth):
    sql = "insert into sys_user(ORG_ID, CLIENT_ID, UserName, Password, REAL_NAME,SEX, " \
          "EMAIL,PHONE,MOBILE,DESCRIPTION,ISACTIVE,CREATED,CREATEBY,UPDATED,UPDATEBY,REMOVE,DATAFILTER," \
          "theme,defaultpage,logoimage,qqopenid,appversion,jsonauth) " \
          "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
          (0,0,"'" + UserName + "'", "'" + Password + "'","'" + REAL_NAME + "'", "'" + SEX + "'",
           "'" + EMAIL + "'", "'" + PHONE + "'","'" + MOBILE + "'","'" + DESCRIPTION + "'","'" + ISACTIVE + "'","'" + CREATED + "'"
           ,CREATEBY,"'" + UPDATED + "'",UPDATEBY,"'" + REMOVE + "'","'" + DATAFILTER + "'","'" + theme + "'","'" + defaultpage + "'"
           ,"'" + logoimage + "'","'" + qqopenid + "'","'" + appversion + "'","'" + jsonauth + "'")
    print(sql)
    connect.executeSql(sql)

#delete
def deleteVolunteer(id):
    sql = "delete from sys_user where id=" + str(id)
    connect.executeSql(sql)

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
#addUser(0,0,"user","123456","WANG","boy","email@123","112234","123456","good","yes",now,12,now,12,'n',"null",
        #"theme","defaultpage","loginimage","qqopenid","appversion","json")
#deleteVolunteer(63)
#updateVolunteer(1,"HHH")