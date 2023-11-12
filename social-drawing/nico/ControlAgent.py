import numpy as np
from agentspace import Agent, space
import time 

class ControlAgent(Agent):

    def __init__(self, namePoints, nameFacePoint, namePoint):
        self.namePoints = namePoints
        self.nameFacePoint = nameFacePoint
        self.namePoint = namePoint
        super().__init__()

    def init(self):
        self.attention = 2
        space.attach_trigger(self.namePoints,self)
        space.attach_trigger(self.nameFacePoint,self)
        
    def senseSelectAct(self):
        mode = space(default=0)['mode']
        if mode == 0:
            return
        elif mode == 1:
            point = space[self.nameFacePoint]
            space(validity=0.5)[self.namePoint] = point
        elif mode == 2:
            points = space[self.namePoints]
            if points is not None:
                if np.random.uniform(0,1) > 0.985:
                    self.attention = np.random.randint(6)
                point = points[self.attention]
                space(validity=0.5)[self.namePoint] = point
