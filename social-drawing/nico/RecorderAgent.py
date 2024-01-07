import os
import numpy as np
import cv2
from nico.agentspace import Agent, space, Trigger
from datetime import datetime

class RecorderAgent(Agent):

    def init(self):
        self.lastName = ""
        self.number = 0
        self.out = None
        self.fps = 10
        self.size = (1280,960)
        self.hsize = (self.size[0]//2,self.size[1]//2)
        self.blank = np.zeros((self.hsize[1],self.hsize[0],3),np.uint8)
        self.filename = ""
        self.attach_timer(1.0/self.fps)
        space.attach_trigger('filename',self,Trigger.NAMES)
        
    def senseSelectAct(self):
        if self.triggered() == 'filename':
            filename = space(default="")['filename']
            if filename == self.filename:
                return
            self.filename = filename
            if self.out is not None:
                self.out.release()
                self.out = None
            if filename == "":
                return
            try:
                os.mkdir("video/")
            except FileExistsError: 
                pass
            self.out = cv2.VideoWriter()
            self.out.open("video/" + filename + ".avi",cv2.VideoWriter_fourcc('M','J','P','G'),self.fps,self.size)
        else:
            if self.out is not None:
                tl = cv2.resize(space(default=self.blank)['humanImage'],self.hsize)
                tr = cv2.resize(space(default=self.blank)['robotImage'],self.hsize)
                bl = cv2.resize(space(default=self.blank)['camera'],self.hsize) #np.copy(self.blank)
                br = cv2.resize(space(default=self.blank)['wide camera'],self.hsize)
                cv2.putText(br,str(datetime.now())[:22],(10,self.hsize[1]-15),0,1.0,(255,255,255),1)
                frame = cv2.vconcat([cv2.hconcat([tl,tr]),cv2.hconcat([bl,br])])
                self.out.write(frame)
