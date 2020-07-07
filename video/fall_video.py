import cv2
# 读取视频文件
from event_ws import event_handle

# cap = cv2.VideoCapture('F:\\Pycharm_project\\care_sys\\version\\falldown\\fall.mp4')

# k=0
# while k < cap.get(7):
#     success,frame = cap.read()
#     if not success:
#         break
#     event_handle.detect_fall(frame)
#     k = k + 1
#
#     if cv2.waitKey(33) == 27:
#         break
#
# cv2.destroyAllWindows()
