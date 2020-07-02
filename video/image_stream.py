import base64
import cv2


# 视频流
def image_stream(img_local_path):
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


def cv_photo():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()

        cv2.imshow('jiankong', frame)
        cv2.imwrite('static/images/temp.jpg', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            break
        elif key == 27:
            break
    cv2.destroyAllWindows()
    camera.release()
