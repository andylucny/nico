import numpy as np
import cv2
import time

camera = cv2.VideoCapture(0,cv2.CAP_DSHOW) #1
#camera = cv2.VideoCapture("http://208.72.70.171/mjpg/video.mjpg")
cv2.namedWindow('camera',cv2.WINDOW_NORMAL)

while True:
    hasFrame, frame = camera.read()
    if not hasFrame:
        break
    cv2.imshow('camera',frame)
    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == ord('s'):
        name = str(round(time.time()))
        cv2.imwrite(name+'.png',frame)

camera.release()
cv2.destroyAllWindows()
