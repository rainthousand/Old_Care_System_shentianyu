import numpy as np
import cv2
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

global_frame = None

def contrast_brightness(image, c, b):  # 其中c为对比度，b为每个像素加上的值（调节亮度）
    blank = np.zeros(image.shape, image.dtype)  # 创建一张与原图像大小及通道数都相同的黑色图像
    dst = cv2.addWeighted(image, c, blank, 1 - c, b)  # c为加权值，b为每个像素所加的像素值
    ret, dst = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)
    return dst


def drawfire(image, fireimage):
    _, contours, hierarchy = cv2.findContours(fireimage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    max_cnt = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > max_area):
            max_area = area
            max_cnt = cnt

    if (max_area != 0):
        x, y, w, h = cv2.boundingRect(max_cnt)
        #        cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 1)
        rect = cv2.minAreaRect(max_cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
    if (max_area != 0):
        cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
    cv2.imshow("img", image)


def drawfire_bak(frame, fireimage):
    global global_frame
    sign=False
    display_str = str('Fire')
    image_np = Image.fromarray(frame)
    draw = ImageDraw.Draw(image_np)
    contours, hierarchy = cv2.findContours(fireimage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    v_box = []
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if area > 1:
            v_box.append([x, y])
            v_box.append([x + w, y + h])

    if (len(v_box) > 0):
        v_box = np.array(v_box)
        minvx, minvy = np.amin(v_box, axis=0)
        maxvx, maxvy = np.amax(v_box, axis=0)

    if (len(v_box) > 0):
        font = ImageFont.truetype('simhei.ttf', 20, encoding='utf-8')
        display_str_height = font.getsize(display_str)[1]
        display_str_heights = (1 + 2 * 0.05) * display_str_height
        if minvy > display_str_heights:
            text_bottom = minvy
        else:
            text_bottom = maxvy
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle(
            [(minvx, text_bottom - text_height - 2 * margin),
             (minvx + text_width, text_bottom)], fill='blue')
        draw.text(
            (minvx + margin, text_bottom - text_height - margin),
            display_str, fill='yellow', font=font)
        frame = np.array(image_np)
        sign=True
        cv2.rectangle(frame, (minvx, minvy), (maxvx, maxvy), (0, 255, 0), 1)
    # cv2.imshow("img", frame)

    return frame,sign


def fireDetect(dir):
    # capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture(dir)
    temparray = dir.split(".")
    temparray[0] = temparray[0] + "_new"
    tempstr = temparray[0] + "." + temparray[1]

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = capture.get(cv2.CAP_PROP_FPS)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    out = cv2.VideoWriter(tempstr, fourcc, fps, size)

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    redThre = 135
    saturationTh = 55
    ctrl = 2
    ##二帧差分
    if (ctrl == 2):
        frameNum = 0
        while (True):
            ret, frame = capture.read()
            frameNum += 1
            if ret == True:
                tempframe = frame
                if (frameNum == 1):
                    previousframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
                if (frameNum >= 2):
                    currentframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
                    currentframe = cv2.absdiff(currentframe, previousframe)
                    median = cv2.medianBlur(currentframe, 3)
                    ret, threshold_frame = cv2.threshold(currentframe, 20, 255, cv2.THRESH_BINARY)
                    mask_inv = cv2.bitwise_not(threshold_frame)
                    gauss_image = cv2.GaussianBlur(threshold_frame, (3, 3), 0)

                    B = frame[:, :, 0]
                    G = frame[:, :, 1]
                    R = frame[:, :, 2]
                    minValue = np.array(np.where(R <= G, np.where(G < B, R,
                                                                  np.where(R < B, R, B)), np.where(G < B, G, B)))
                    S = 1 - 3.0 * minValue / (R + G + B)
                    #                    fireImg = np.array(np.where(R > redThre,
                    #                                                np.where(R > G,
                    #                                                         np.where(G > B,
                    #                                                                  np.where(S > 0.2,
                    #                                                                           np.where(S > (255 - R)*saturationTh/redThre, 255, 0), 0), 0), 0), 0))
                    fireImg = np.array(np.where(R > redThre,
                                                np.where(R > G,
                                                         np.where(G > B,
                                                                  np.where(S > (255 - R) * saturationTh / redThre,
                                                                           255,
                                                                           0), 0), 0), 0))

                    gray_fireImg = np.zeros([fireImg.shape[0], fireImg.shape[1], 1], np.uint8)
                    gray_fireImg[:, :, 0] = fireImg
                    gray_fireImg = cv2.GaussianBlur(gray_fireImg, (3, 3), 0)

                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    #                    gray_fireImg = cv2.morphologyEx(gray_fireImg, cv2.MORPH_CLOSE, kernel)
                    gauss_image = cv2.morphologyEx(gauss_image, cv2.MORPH_OPEN, kernel)
                    cv2.imshow("gauss_image", gauss_image)
                    #                    TOPHAT_img = cv2.morphologyEx(gray_fireImg, cv2.MORPH_TOPHAT, kernel)
                    #                    BLACKHAT_img = cv2.morphologyEx(gray_fireImg, cv2.MORPH_BLACKHAT, kernel)
                    #                    bitwiseXor_gray = cv2.bitwise_xor(gray_fireImg,TOPHAT_img)

                    gray_fireImg = contrast_brightness(gray_fireImg, 5., 25)
                    cv2.imshow("gray_fireImg", gray_fireImg)
                    #                    gray_fireImg = cv2.bitwise_not(gray_fireImg)
                    gray_fireImg = cv2.bitwise_and(gray_fireImg, gauss_image, mask=mask_inv)

                    frame, sign=drawfire_bak(frame, gray_fireImg)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                previousframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)

                out.write(frame)

                # if frame is not None:
                #     global_frame = frame
                #     yield (b'--frame\r\n'
                #            b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes()
                #            + b'\r\n\r\n')
                # else:
                #     yield (b'--frame\r\n'
                #            b'Content-Type: image/jpeg\r\n\r\n'
                #            + global_frame + b'\r\n\r\n')
            else:
                break


if __name__ == '__main__':
    fireDetect("fire.mp4")
       # capture = cv2.VideoCapture("fire.mp4")
    # capture = cv2.VideoCapture(0)