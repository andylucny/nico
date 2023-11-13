import numpy as np
from nico.agentspace import Agent, space
import cv2 as cv
import time

class ViewerAgent(Agent):

    def __init__(self, nameImage, nameWideImage, namePoints, nameFacePoint, namePoint):
        self.nameImage = nameImage
        self.nameWideImage = nameWideImage
        self.namePoints = namePoints
        self.nameFacePoint = nameFacePoint
        self.namePoint = namePoint
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameImage,self)
            
    def senseSelectAct(self):
        image = space[self.nameImage]
        wideimage = space[self.nameWideImage]
        if image is None:
            return
        image = np.copy(image)
        if wideimage is None:
            wideimage = np.copy(image)
        else:
            wideimage = np.copy(wideimage)
        #image = cv.resize(image,(image.shape[1]//2,image.shape[0]//2))
        wideimage = cv.resize(wideimage,(image.shape[1],image.shape[0]))

        current = space[self.namePoint]
        
        points = space(default=[])[self.namePoints]
        for i, point in enumerate(points):
            if point[0] >= 0.0 and point[1] >= 0.0:
                color = (0,0,255) if point == current else (0,255,0)
                pt = (int(point[0]*image.shape[1]),int(point[1]*image.shape[0]))
                cv.circle(image,pt,3,color,cv.FILLED)
                cv.putText(image,str(i),(pt[0],pt[1]-5),0,1.0,color,1)

        face = space[self.nameFacePoint]
        if face is not None:
            color = (0,0,255) if face == current else (0,255,0)
            pt = (int(face[0]*wideimage.shape[1]),int(face[1]*wideimage.shape[0]))
            cv.circle(wideimage,pt,10,color,cv.FILLED)
        
        cv.imshow("camera",cv.hconcat([image,wideimage]))
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite('righteye'+str(time.time())+'.png',image)
            cv.imwrite('lefteye'+str(time.time())+'.png',wideimage)
