import cv2

def smileDetect(img):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')#人脸
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')#人眼
    smile_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')#微笑
    sign = False

    # 6灰度处理
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 7检查人脸
    faces = face_cascade.detectMultiScale(gray, 1.1, 3, 0, (120, 120))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
        face_area = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(face_area,1.3,10)
        # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
        for (ex, ey, ew, eh) in eyes:
            # 画出人眼框，绿色，画笔宽度为1
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

        smile = smile_cascade.detectMultiScale(face_area, scaleFactor=1.16, minNeighbors=50, minSize=(50, 50),
                                               flags=cv2.CASCADE_SCALE_IMAGE)
        # 用微笑级联分类器引擎在人脸区域进行人眼识别，返回的smile为微笑坐标列表
        for (ex, ey, ew, eh) in smile:
            # 画出微笑框，绿色，画笔宽度为1
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
            cv2.putText(img, 'Smile', (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
            sign = True

    return img, sign

def smileDetect2():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')#人脸
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')#人眼
    smile_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')#微笑

    framelist=[]

    #3打开摄像头
    capture=cv2.VideoCapture(0)

    while True:
        #读取该帧的画面
        ret, img = capture.read()
        # 6灰度处理
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # 7检查人脸
        faces = face_cascade.detectMultiScale(gray, 1.1, 3, 0, (120, 120))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
            face_area = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(face_area,1.3,10)
            # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
            for (ex, ey, ew, eh) in eyes:
                # 画出人眼框，绿色，画笔宽度为1
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

            smile = smile_cascade.detectMultiScale(face_area, scaleFactor=1.16, minNeighbors=50, minSize=(50, 50),
                                               flags=cv2.CASCADE_SCALE_IMAGE)
            # 用微笑级联分类器引擎在人脸区域进行人眼识别，返回的smile为微笑坐标列表
            for (ex, ey, ew, eh) in smile:
                # 画出微笑框，绿色，画笔宽度为1
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
                cv2.putText(img, 'Smile', (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
        # 9显示图片
        cv2.imshow("test", img)
        framelist.append(img)
        # 10暂停窗口
        if cv2.waitKey(33) == 27:
            break
    #11释放资源
    capture.release()
    # #12销毁窗口
    cv2.destroyAllWindows()

    return framelist

if __name__ == '__main__':
    # templist = fallDetect("falldown/fall2.mp4")
    templist = smileDetect2()
    print(len(templist))
    # fallDetect("falldown/fall1.mp4")