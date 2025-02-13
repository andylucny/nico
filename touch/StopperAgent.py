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
        rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y','r_wrist_z','r_wrist_x','r_thumb_z','r_thumb_x','r_indexfinger_x','r_middlefingers_x']
        stopAllMotors(rightArmDofs)
