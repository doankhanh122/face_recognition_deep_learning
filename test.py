import imutils.paths as paths
import face_recognition
import argparse
import pickle
import cv2 as cv
import os
from encode_faces_after_save import encoding_face

# name ="kim_thi_mai_huong"
data = pickle.loads(open("encodings.pickle", 'rb').read())
# data = pickle.loads(open("encodings.pickle", 'rb').read())
print(data)
#
# image_paths = list(paths.list_images(f"dataset/{name}"))

# for (i, imagePath) in enumerate(image_paths):
    # extract the person name from the image path
    # print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))


    # print(imagePath)
