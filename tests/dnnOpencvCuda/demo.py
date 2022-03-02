#import easyocr
import numpy as np
import cv2
import time
#from bgremover import bgremover
from faceDetector import faceDetector
#from ocr import textDetector
from faceRecognizer import faceRecognizer

#bg = bgremover()
fd = faceDetector()
#td = textDetector()
fr = faceRecognizer()

camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)

status = 0
while True:
    hasFrame, frame = camera.read()
    if not hasFrame:
        break
        
    if status == 0:
        disp = frame
    elif status == 1:
        #_, disp = bg.process(frame)
        disp = frame
    elif status == 2:
        disp, _ = bg.process(frame)
    elif status == 3:
        disp, _ = fd.process(frame)
    elif status == 4:
        disp, face = fd.process(frame)
        if face is not None:
            disp, _ = fr.process(disp,face)
#    elif status == 5:
#        disp = td.process(frame)
        
    cv2.imshow('camera',disp)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('s'):
        name = str(round(time.time()))
        cv2.imwrite(name+'.png',disp)
    elif key == ord('0'):
        status = 0
    elif key == ord('1'):
        status = 1
    elif key == ord('2'):
        status = 2
    elif key == ord('3'):
        status = 3
    elif key == ord('4'):
        status = 4
    elif key == ord('5'):
        status = 5

camera.release()
cv2.destroyAllWindows()
