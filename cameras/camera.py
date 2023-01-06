import numpy as np
import cv2
import time

Lcamera = cv2.VideoCapture(0,cv2.CAP_DSHOW) # left eye
Rcamera = cv2.VideoCapture(2,cv2.CAP_DSHOW) # right eye
#cv2.namedWindow('camera',cv2.WINDOW_NORMAL)

fps = 30 # to je jedno co, ale musi sa to nastavit
Lcamera.set(cv2.CAP_PROP_FPS,fps)    
Rcamera.set(cv2.CAP_PROP_FPS,fps)    
print(fps,'fps')
_, frameL = Lcamera.read()
_, frameR = Rcamera.read()

frame = cv2.hconcat([frameL,frameR])

out = cv2.VideoWriter()
out.open('record.avi',cv2.VideoWriter_fourcc('M','J','P','G'),fps,(frame.shape[1],frame.shape[0]))

t0 = int(time.time())
fps = 0
while True:
    cv2.imshow('camera',frame)
    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == ord('s'):
        name = str(round(time.time()))
        cv2.imwrite(name+'-left.png',frameL)
        cv2.imwrite(name+'-right.png',frameR)
        
    out.write(frame)

    hasFrameL, frameL = Lcamera.read()
    hasFrameR, frameR = Rcamera.read()
    fps += 1
    t1 = int(time.time())
    if t1 != t0:
        print('fps',fps)
        t0 = t1
        fps = 0

    if not hasFrameL and not hasFrameR:
        break

    frame = cv2.hconcat([frameL,frameR])
        
out.release()
Lcamera.release()
Rcamera.release()
cv2.destroyAllWindows()
