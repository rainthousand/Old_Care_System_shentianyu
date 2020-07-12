import cv2


def get_img_from_camera_net():
    cap = cv2.VideoCapture("rtmp://192.168.0.17:1935/live/home")  # 获取网络摄像机

    while True:
        ret, frame = cap.read()
        break

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()


# 测试
if __name__ == '__main__':
    get_img_from_camera_net()