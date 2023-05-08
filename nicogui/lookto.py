import numpy as np
import cv2
from nicomotors import NicoMotors
from nicocameras import NicoCameras
import time
import os
import signal 

def quit():
    os._exit(0)
    
# exit on ctrl-c
def signal_handler(signal, frame):
    quit()

motors = NicoMotors()
dofs = motors.dofs()
motors.open()
headDofs = dofs[-2:]

def getHead():
    angles = []
    for dof in headDofs:
        angle = motors.getPositionDg(dof)
        angles.append(angle)
    return angles

head = getHead()

def setHead(angles):
	for dof,angle in zip(headDofs,angles):
		motors.setPositionDg(dof,angle)
        
def colorFilter(bgr):
    # converting from BGR to HSV color space
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # filtering in HSV
    lowerLimit = np.array([160,100,25],np.uint8)
    upperLimit = np.array([180,255,255],np.uint8)
    mask1 = cv2.inRange(hsv, lowerLimit, upperLimit)
    lowerLimit = np.array([0,100,25],np.uint8)
    upperLimit = np.array([10,255,255],np.uint8)
    mask2 = cv2.inRange(hsv, lowerLimit, upperLimit)
    mask = mask1
    # redraw the detected ball
    indices = np.where(mask > 0)
    bgr[indices[0],indices[1],:] = [255,255,0]
    # if pixel number of ball is too small, it is perhaps not the ball at all
    if np.shape(indices)[1] < 10:
        # ball not found
        return None
    else:
        # return average of x and y coordinates of pixels
        return (int(np.average(indices[1])),int(np.average(indices[0])))

cameras = NicoCameras()
time.sleep(1)
eps = 0.05
delta = 1
while True:
    leftImage, rightImage = cameras.read()
    if leftImage is None or rightImage is None:
        time.sleep(0.1)
        continue
    leftPos = colorFilter(leftImage)
    rightPos = colorFilter(rightImage)
    if leftPos is not None:
        cv2.circle(leftImage,leftPos,5,(0,0,255),cv2.FILLED)
    if rightPos is not None:
        cv2.circle(rightImage,rightPos,5,(0,0,255),cv2.FILLED)
    cv2.imshow("nico",cv2.hconcat([leftImage, rightImage]))
    if cv2.waitKey(1) == 27:
        break
    if leftPos is None or rightPos is None:
        continue
    leftPos = np.array(leftPos)/np.array(leftImage.shape[:2][::-1])
    rightPos = np.array(rightPos)/np.array(rightImage.shape[:2][::-1])
    pos = (leftPos+rightPos)/2
    if pos[0] < 0.5 - eps:
        head[1] -= delta
    elif pos[0] > 0.5 + eps:
        head[1] += delta
    if pos[1] < 0.7 - eps:
        head[0] += delta
    elif pos[1] > 0.7 + eps:
        head[0] -= delta
    print(head)
    setHead(head)
    time.sleep(0.5)
    head = getHead()    
