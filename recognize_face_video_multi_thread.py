# import
# from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
# import cv2 as cv
import concurrent.futures
from functions import *

# construct the argument parser and parser the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str, help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
                help="whether or not display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default='hog',
                help="face detection model to use: either 'hog' or 'cnn' ")

args = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], 'rb').read(),)


# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
writer = None
time.sleep(2.0)

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
    frame = vs.read()

    # convert the input frame from BGR to RGB then resize it to have
    # a width of 750px (to speedup processing)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)
    r = frame.shape[1] / float(rgb.shape[1])

    # detect the (x,y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(faces_locate, rgb, args["detection_method"])
        # print(future.result())
        boxes = future.result()
    # boxes = face_recognition.face_locations(rgb, model=args["detection_method"])

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial encodings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        distance = face_recognition.face_distance(data["encodings"], encoding)

        rate = round(max(distance), 2)
        print(max(distance))
        name = "Unknown"

        # check to see if we have
        # found a match
        if True in matches:
            # find the index of all matched faces then initialeze a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary
            name = max(counts, key=counts.get)

        # update the list of name
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # rescale the face coordinates
        top = int(top*r)

        right = int(right*r)
        bottom = int(bottom*r)
        left = int(left*r)

        # draw the pridicted face name on the image
        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 0 else top + 15
        # cv.rectangle(frame, (left-1, top), (right+1, top - 15), (0, 255, 0), thickness=-1)
        cv.putText(frame, f"Rate: {rate} / {name}", (left, y), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # if the video writer is None *AND* we are supposed to write
    # the output video to disk initialize the writer
    if writer is None and args['output'] is not None:
        fourcc = cv.VideoWriter_fourcc(*"MJPG")
        writer = cv.VideoWriter(args["output"],
                                fourcc, 20, (frame.shape[1], frame.shape[0]), True)

    # if the writer is not None, write the frame with recognized
    # faces to disk
    if writer is not None:
        writer.write(frame)

    # check to see if we are supposed to display the output frame to
    # the screen
    if args['display'] > 0:
        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF

        # if the 'q' key was pressed, break from the loop
        if key == ord("q"):
            break

# do a bit of cleanup
cv.destroyAllWindows()
vs.stop()

# check to see if the video writer point needse to be released
if writer is not None:
    writer.release()
