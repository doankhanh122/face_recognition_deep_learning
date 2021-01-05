import imutils.paths as paths
import face_recognition
import argparse
import pickle
import cv2 as cv
import os
import concurrent.futures
import time



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True, help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True, help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help=" face detection model to use: either 'hog' or 'cnn'")

args = vars(ap.parse_args())


# grab the paths to the input images in our dataset
print(" [INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))


# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []


# loop over the image paths
def encoding_faces(image_path):

    # extract the person name from the image path
    print("[INFO] processing image {}/{}".format(imagePaths.index(image_path)+1, len(imagePaths)))

    name = image_path.split(os.path.sep)[-2]
    print(f'[INFO] get name success {name}')

    # load the input image and convert it from BGR to RGB
    # to dlib ordering (RGB)
    image = cv.imread(image_path)

    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    print(f'[INFO] convert to RGB success')
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
    print(f'[INFO] face detection success {boxes}')
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    print(f'[INFO] encoding success {encodings}')
    # loop over the encodings
    for encoding in encodings:
        # add each encoding + name to our set of known names and
        # encodings
        knownEncodings.append(encoding)
        knownNames.append(name)


encoding_faces(imagePaths[0])
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(encoding_faces, imagePaths)
#     # for (i, imagePath) in enumerate(imagePaths):
#     #     executor.submit(encoding_faces, imagePath, i)

# dump the facial encodings + name to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
print(data)
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()





