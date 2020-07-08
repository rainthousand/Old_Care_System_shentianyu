import cv2
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, render_template, Response, request, redirect, url_for, abort, session
from flask import request, Flask
import base64
import cv2
import numpy as np

from config import config_dict


config_class = config_dict['dev']
app = Flask(__name__)
app.config.from_object(config_class)
user_socket_list = []

@app.route('/getvideo', methods=['GET', 'POST'])
def getvideo():
    camera = cv2.VideoCapture(0)
    while True:
        ret,frame = camera.read()

        if frame is None:
            print("none!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            cv2.imshow("video",frame)

        base64_data = base64.b64encode(frame)
        imgData = base64.b64decode(base64_data)
        nparr = np.fromstring(imgData, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        image = cv2.imencode('.jpg', img_np)[1]
        frame = str(base64.b64encode(image))[2:-1]
        # if cv2.waitKey(33) == 27:
        #     break

        return frame
    # 11释放资源
    camera.release()

# #图片流
# @app.route('/test')
# def img_stream():
#     img_path = 'static/images/bg1.jpg'
#     img_stream = image_stream.image_stream(img_path)
#
#     return render_template('test.html', img_stream=img_stream)

# 主界面


# ____________________________________________________________________________________________manager


if __name__ == '__main__':
    # app.run(host='0.0.0.0', threaded=True)
    server = pywsgi.WSGIServer(('127.0.0.1', 6000), app, handler_class=WebSocketHandler)
    if server:
        print('server start!!!!!!!!!')
    else:
        print("ERROR")
    server.serve_forever()
