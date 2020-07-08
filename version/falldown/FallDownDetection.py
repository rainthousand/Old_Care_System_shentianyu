import cv2
import time

global_frame = None
# j = 0
def fallDetect(frame):

    # cap = cv2.VideoCapture(dir)
    # time.sleep(2)
    sign=False
    typesign = ""

    fgbg = cv2.createBackgroundSubtractorMOG2()
    j = 0
    # global j
    # Conver each frame to gray scale and subtract the background
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    cv2.imshow("gray",gray)

    # Find contours
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        areas = []

        for contour in contours:
            ar = cv2.contourArea(contour)
            areas.append(ar)
            print(ar)

        max_area = max(areas or [0])

        max_area_index = areas.index(max_area)

        cnt = contours[max_area_index]

        M = cv2.moments(cnt)

        x, y, w, h = cv2.boundingRect(cnt)
        print("x:"+str(x)+",y:"+str(y)+",w:"+str(w)+",h:"+str(w))

        cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

        if h < w:
            j += 1
            print("fall:"+str(j))
            # print(j)

        if j > 10:
            # print "FALL"
            # cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            sign = True
            # cv2.imshow("test", frame)

        if h > w:
            j = 0
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("notfall:"+str(j))

    return frame, sign, j


def fallDetect2(dir):

    cap = cv2.VideoCapture(dir)
    time.sleep(2)
    print(";;;;;;;")
    print(cap.get(7))
    global global_frame
    # cap = cv2.VideoCapture(0)

    fgbg = cv2.createBackgroundSubtractorMOG2()
    j = 0
    print(type(cap))
    print(dir)
    temparray = dir.split(".")
    temparray[0] = temparray[0] + "_new"
    tempstr = temparray[0] + "." + temparray[1]

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    out = cv2.VideoWriter(tempstr, fourcc, fps, size)

    # framelist=[]

    k=0

    while k < cap.get(7):
        # print("-----")
        ret, frame = cap.read()

        # Conver each frame to gray scale and subtract the background
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)

        # Find contours
        contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)

            max_area = max(areas or [0])

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)

            x, y, w, h = cv2.boundingRect(cnt)
            print("x:" + str(x) + ",y:" + str(y) + ",w:" + str(w) + ",h:" + str(w))

            cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

            if h < w:
                j += 1
                print(j)

            if j > 10:
                # print "FALL"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2)

            if h > w:
                j = 0
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 写入一帧
            out.write(frame)
            # framelist.append(frame)

            # cv2.imshow('video', frame)

            k=k+1
            # if frame is not None:
            #     global_frame = frame
            #     yield (b'--frame\r\n'
            #            b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes()
            #            + b'\r\n\r\n')
            # else:
            #     yield (b'--frame\r\n'
            #            b'Content-Type: image/jpeg\r\n\r\n'
            #            + global_frame + b'\r\n\r\n')

            if cv2.waitKey(33) == 27:
                break
    cv2.destroyAllWindows()

    # return framelist


if __name__ == '__main__':
    # templist = fallDetect("falldown/fall2.mp4")
    # print(len(templist))
    # fallDetect("falldown/fall1.mp4")
    fallDetect2('F:\\Pycharm_project\\care_sys\\version\\falldown\\fall.mp4')