import numpy as np
import cv2
import time

Lcamera = cv2.VideoCapture(0) # left eye
Rcamera = cv2.VideoCapture(1) # right eye
cv2.namedWindow('camera',cv2.WINDOW_NORMAL)

fps=10
camera.set(cv2.CAP_PROP_FPS,fps)    
print(fps,'fps')
_, frameL = Lcamera.read()
_, frameR = Rcamera.read()

frame = cv2.hconcat([frameL,frameR])

out = cv2.VideoWriter()
out.open('../record.avi',cv2.VideoWriter_fourcc('M','J','P','G'),fps,(frame.shape[1],frame.shape[0]))

while True:
    cv2.imshow('camera',frame)
    key = cv2.waitKey(10)
    if key == 27:
        break

    out.write(frame)

    hasFrameL, frameL = Lcamera.read()
    hasFrameR, frameR = Rcamera.read()

    if not hasFrameL and not hasFrameR:
        break

    frame = cv2.hconcat([frameL,frameR])
        
out.release()
camera.release()
cv2.destroyAllWindows()
