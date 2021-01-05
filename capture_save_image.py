import cv2 as cv
import face_recognition
import argparse
import os
from encode_faces_after_save import encoding_face
import time
# import imutils.paths as paths
import pickle

data = pickle.loads(open("encodings.pickle", 'rb').read())
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", type=str, required=True, help="Type person's name to save to dataset")

args = vars(ap.parse_args())

os.mkdir(f"dataset/{args['name']}")

webcam = cv.VideoCapture(0, cv.CAP_DSHOW)
img_count = 0

while img_count < 20:
    time.sleep(0.25)
    success, frame = webcam.read()
    cv.imshow("Webcam", frame)

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)

    if len(face_locations) == 1:
        for (top, right, bottom, left) in face_locations:
            # print(x, y, h, w)
            face = frame[top:bottom, left:right]
            cv.imwrite(f"dataset/{args['name']}/{args['name']}_{img_count}.jpg", face)
            img_count += 1
    elif len(face_locations) > 1:
        print("Only one person one time!")
    else:
        pass

    key = cv.waitKey(1)
    if key == ord("q"):
        break

new_data = encoding_face(args['name'], data)
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(new_data))
f.close()
# print(new_data)
print("[INFO] Finish encoding")
