from agentspace import Agent, space
from mover3 import stopAllMotors
import numpy as np
import time
        
class StopperAgent(Agent):
            
    def init(self):
        space.attach_trigger("touch",self)

    def senseSelectAct(self):
        point = space["touch"]
        if point is None:
            return
        if point[0] < 0 or point[1] < 0:
            return

        space["stop"] = True
        stopAllMotors()
