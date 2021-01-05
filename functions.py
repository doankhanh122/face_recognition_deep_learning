import face_recognition
import cv2 as cv
from imutils.video import VideoStream
import threading
exitFlag = 0
threadingLock = threading.Lock()
threads = []


class CreateThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        threadingLock.acquire()
        encoding_face(self.name, 5, self.counter)
        # Free lock to release next thread
        threadingLock.release()
        print("Exiting " + self.name)


def encoding_face(data, encodings):
    names = []
    for encoding in encodings:
        matches = face_recognition.face_encodings(data["encodings"], encoding)

        if True in matches:

            # find the index of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matched_index_list = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matched_index_list:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary
            name = max(counts, key=counts.get)

        names.append(name)
    return names


def faces_locate(rgb_img, model_rec):
    locations = face_recognition.face_locations(rgb_img, model=model_rec)
    return locations


def live_webcam():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    while True:
        frame = vs.read()
        cv.imshow("Webcam", frame)

        cv.waitKey(1)
