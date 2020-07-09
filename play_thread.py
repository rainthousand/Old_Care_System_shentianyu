import threading,time

from playsound import playsound

from version.collect import collectingfaces


def run():
    print(collectingfaces.global_signal)
    if collectingfaces.global_signal == 0:
        time.sleep(2)
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\blink.mp3")
    elif collectingfaces.global_signal == 1:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\open_mouth.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 2:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\smile.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 3:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\rise_head.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 4:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\bow_head.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 5:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\look_left.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 6:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\look_right.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 7:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\no_face_detected.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 8:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\start_image_capturing.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 9:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\multi_faces_detected.mp3")
        time.sleep(2)
    elif collectingfaces.global_signal == 10:
        playsound("F:\\Pycharm_project\\care_sys\\version\\audios\\end_capturing.mp3")
        time.sleep(2)