import cv2
# 读取视频文件
from event_ws import event_handle

cap = cv2.VideoCapture('E:\\PythonProjects\\Old_Care_System_shentianyu\\vision\\falldown\\fall3.mp4')
# 或者电影每秒的帧数
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
# 判断视频是否一直打开
k=0
# j=0
while k < cap.get(7):
    success,frame = cap.read()
    if not success:
        break
    frame = event_handle.detect_fall(frame)
    # 视频显示
    # cv2.imshow('falldown', frame)
    # # 设置窗口
    # cv2.resizeWindow('law', 512,288)
    # 判断退出条件
    k = k + 1

    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()