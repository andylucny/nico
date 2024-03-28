import numpy as np
from nico.agentspace import Agent, space
import cv2 as cv
import time

class ViewerAgent(Agent):

    def __init__(self, nameSideImage1, nameSideImage2, nameImage, nameWideImage, namePoints, nameFacePoint, namePoint):
        self.nameSideImage1 = nameSideImage1
        self.nameSideImage2 = nameSideImage2
        self.nameImage = nameImage
        self.nameWideImage = nameWideImage
        self.namePoints = namePoints
        self.nameFacePoint = nameFacePoint
        self.namePoint = namePoint
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameSideImage1,self)
            
    def senseSelectAct(self):
        image1 = space[self.nameSideImage1]
        if image1 is None:
            return
        blank = np.zeros_like(image1)
        image2 = space(default=blank)[self.nameSideImage2]
        image = space(default=blank)[self.nameImage]
        wideimage = space(default=blank)[self.nameWideImage]
        image = np.copy(image)
        if wideimage is None:
            wideimage = np.copy(image)
        else:
            wideimage = np.copy(wideimage)
        image2 = cv.resize(image2,(image1.shape[1],image1.shape[0]))
        image = cv.resize(image,(image1.shape[1],image1.shape[0]))
        wideimage = cv.resize(wideimage,(image1.shape[1],image1.shape[0]))

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
 
        result = cv.vconcat([cv.hconcat([image1,image2]),cv.hconcat([image,wideimage])])
        result = cv.resize(result,(image1.shape[1],image1.shape[0]))
        cv.imshow("camera",result)
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite('righteye'+str(time.time())+'.png',image)
            cv.imwrite('lefteye'+str(time.time())+'.png',wideimage)
