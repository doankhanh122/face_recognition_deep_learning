import imutils.paths as paths
import face_recognition
# import argparse
# import pickle
import cv2 as cv
# import os


def encoding_face(name, data):
    # data = pickle.loads(open("encodings_3.pickle", 'rb').read())
    # data = pickle.loads(open("encodings.pickle", "wb"))
    # print(data)

    # grab the paths to the input images in our dataset
    print(" [INFO] quantifying faces...")

    image_paths = list(paths.list_images(f"dataset/{name}"))
    # print(image_paths)

    # initialize the list of known encodings and known names
    # knownEncodings = []
    # knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(image_paths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i+1, len(image_paths)))
    #
    #     name = imagePath.split(os.path.sep)[-3]
    #     print(name)
    # #
    #     # load the input image and convert it from BGR to RGB
    #     # to dlib ordering (RGB)
        image = cv.imread(imagePath)
    #
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            data["encodings"].append(encoding)
            data["names"].append(name)
    # print(data)

    return data
    # dump the facial encodings + name to disk

    # data = {"encodings": knownEncodings, "names": knownNames}
    # f = open("encodings.pickle", "wb")
    # f.write(pickle.dumps(data))
    # f.close()
