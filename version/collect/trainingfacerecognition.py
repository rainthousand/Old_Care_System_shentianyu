# -*- coding: utf-8 -*-

'''
训练人脸识别模型
'''


# import the necessary packages
from imutils import paths
from version.activity.faceutildlib import FaceUtil

# global variable
dataset_path = './image/faces'
output_encoding_file_path = './version/models/face_recognition_hog.pickle'


def training():
    # grab the paths to the input images in our datasets
    print("[INFO] quantifying faces...")
    image_paths = list(paths.list_images(dataset_path))

    if len(image_paths) == 0:
        print('[ERROR] no images to train.')
    else:
        faceutil = FaceUtil()
        print("[INFO] training face embeddings...")
        faceutil.save_embeddings(image_paths, output_encoding_file_path)