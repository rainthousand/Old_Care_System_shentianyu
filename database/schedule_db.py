import datetime
import json
import dateutil.parser as parser
import pymysql
from collections import OrderedDict

db = pymysql.connect(host="47.94.95.94", user="root", passwd="abcd1234", db="project", port=3306, charset='utf8')

conn = db.cursor()
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
print(now)
now_year = parser.parse(now).year
print(now_year)
#select
def getScheduleByUserName(username):
    sql = "select * from schedule where username='"+username+"'"
    print(sql)
    conn.execute(sql)
    result = conn.fetchall()
    jsondata = []
    for em in result:
        data = OrderedDict()
        data['sche_id'] = int(float(em[0]))
        data['sche_name'] = str(em[1])
        data['start_date'] = str(em[2])
        data['end_date'] = str(em[3])
        data['sche_content'] = str(em[4])
        data['username'] = str(em[5])
        jsondata.append(data)
    jsondatas = json.dumps(jsondata, ensure_ascii=False)
    return jsondatas

def addNewSchedule(sche_id,sche_name,start_date,end_date,sche_content,username):
    sql="insert into schedule(sche_id,sche_name,start_date,end_date,sche_content,username) values(%s,%s,%s,%s,%s,%s)" %\
        (sche_id,"'"+sche_name+"'","'"+start_date+"'","'"+end_date+"'","'"+sche_content+"'","'"+username+"'")

    print(sql)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def deleteScheduleByName(sche_name,username):
    sql="delete from schedule where sche_name=%s and username=%s" %\
        ("'"+sche_name+"'","'"+username+"'")

    print(sql)
    try:
        # 执行SQL语句
        conn.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


# print(getScheduleByUserName("wang"))
# addNewSchedule(2,"bbb","2020-07-07","2020-07-09","azczcxzczcx","wang")
deleteScheduleByName("bbb","wang")
