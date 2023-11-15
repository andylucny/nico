from agentspace import Agent, space
import numpy as np
import cv2 as cv
import time
from ExperimentAgent import getHead, changeHead, setHead

class ActionAgent(Agent):

    def __init__(self, namePoint):
        self.namePoint = namePoint
        super().__init__()

    def init(self):
        space.attach_trigger(self.namePoint,self)

    def senseSelectAct(self):
        if space(default=True)['experiment']:
            return
            
        point = space[self.namePoint]
        if point is None:
            return
        
        x, y = point
        
        head_x, head_y = getHead()
        
        delta_degrees_x = np.arctan2((0.5-x)*np.tan(20*np.pi/180),0.5)*180/np.pi
        delta_degrees_y = np.arctan2((0.5-y)*np.tan(20*np.pi/180),0.5)*180/np.pi
        
        angular_speed = 0.04
        limit = 2.0 
        
        dx = 0.0
        if np.abs(delta_degrees_x) > limit:
            candidate = head_x + delta_degrees_x
            if (-30 <= candidate and candidate <= 30) or (candidate < -30 and delta_degrees_x > 0) or (candidate > 30 and delta_degrees_x < 0):
                dx = delta_degrees_x
        dy = 0.0
        if np.abs(delta_degrees_y) > limit:
            candidate = head_y + delta_degrees_y
            if (-10 <= candidate and candidate <= 10) or (candidate < -10 and delta_degrees_x > 0) or (candidate > 10 and delta_degrees_x < 0):
                dy = delta_degrees_y

        changeHead([dx,dy],angular_speed)
        time.sleep(max(np.abs(delta_degrees_x),np.abs(delta_degrees_y))/(1000*angular_speed))
        
