import datetime
import json
import pymysql
import connect
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()
#select
def getEvents():
    sql = "select * from event_info"
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['id'] = int(float(em[0]))
        data['event_type'] = int(float(em[1]))
        data['event_date'] = str(em[2])
        data['event_location'] = str(em[3])
        data['event_desc'] = str(em[4])
        data['oldperson_id'] = int(float(em[5]))

        jsondata.append(data)
    jsondatas = json.dumps(jsondata, ensure_ascii=False)
    return jsondatas

#update
def updateEvent(id,des):
    sql = "update event_info set event_desc='" + des + "' where id="+str(id)

    connect.executeSql(sql)

#add
def addEvent(event_type, event_date, event_location, event_desc, oldperson_id):
    sql = "insert into event_info(event_type, event_date, event_location, event_desc, oldperson_id) " \
          "values(%s,%s,%s,%s,%s)" % \
          (event_type , "'" + event_date + "'","'" + event_location + "'", "'" + event_desc + "'",oldperson_id)
    print(sql)
    connect.executeSql(sql)

#delete
def deleteEvent(id):
    sql = "delete from event_info where id=" + str(id)
    connect.executeSql(sql)

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
#addEvent(0,now,"beside desk","fall off",1)
#deleteVolunteer(63)
#updateVolunteer(1,"HHH")