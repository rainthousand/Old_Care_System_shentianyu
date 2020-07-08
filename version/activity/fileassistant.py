# -*- coding: utf-8 -*-
'''
文件处理相关的函数
'''

import numpy as np
import pandas as pd
import json
import requests

def get_people_info(people_info_path):
    dataset = pd.read_csv(people_info_path)

    # 得到ID->姓名的map
    id_card_to_name = {}
    id_card_to_type = {}
    
    for index, row in dataset.iterrows():
        id_card_to_name[row[0]] = row[1]
        id_card_to_type[row[0]] = row[2]
        
    return id_card_to_name, id_card_to_type
                
def get_facial_expression_info(facial_expression_info_path):
    dataset = pd.read_csv(facial_expression_info_path)

    # 得到摄像头ID->摄像头名字的map
    facial_expression_id_to_name = {}

    for index, row in dataset.iterrows():
        facial_expression_id_to_name[row[0]] = row[1]
        
    return facial_expression_id_to_name
'''
def generate_people_info(people_info_path):
    res = requests.get('http://127.0.0.1:5000/oldpeoplemanagement/api/getinfolist')
    old_people_info_content = res.content.decode('utf-8')
    
    res = requests.get('http://127.0.0.1:5000/employeemanagement/api/getinfolist')
    employee_info_content = res.content.decode('utf-8')
    
    #people_info.bak.csv
    
generate_people_info('')


a = '''
{
  "json_list": [
    {
      "id": 55, 
      "name": "测试"
    }, 
    {
      "id": 57, 
      "name": "工作人员"
    }, 
    {
      "id": 58, 
      "name": "工作人员2"
    }, 
    {
      "id": 59, 
      "name": "工作人员3"
    }
  ]
}
'''
b = json.loads(a)
c = b['json_list']
for i in c:
    print(i['id'], i['name'])
'''    
    