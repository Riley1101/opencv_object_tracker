import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import numpy as np


tracker = cv2.TrackerKCF_create()
video = cv2.VideoCapture('video.mp4')
# video = cv2.VideoCapture(0)
# show output from camera
if not video.isOpened():
    print("INFO : Cannot open camera")
    exit()

ok, frame = video.read()

# select frame from video
bbox = cv2.selectROI(frame)
ok = tracker.init(frame, bbox)
while True:
    ok, frame = video.read()
    if not ok:
        break
    ok, bbox = tracker.update(frame)
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2, 1)
    else:
        cv2.putText(frame, 'Error', (100, 0),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if cv2.waitKey(1) & 0XFF == 27:
        break
cv2.destroyAllWindows()
