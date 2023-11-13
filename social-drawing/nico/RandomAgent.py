from nico.agentspace import Agent, space
import numpy as np
import time

class RandomAgent(Agent):

    def __init__(self, robot):
        self.robot = robot
        super().__init__()

    def init(self):
        self.robot.setAngle("head_z",0.0,0.05)
        self.robot.setAngle("head_y",0.0,0.05)
        time.sleep(2.0)
        self.attach_timer(1.0)

    def senseSelectAct(self):
        if space(default=0)['mode'] != 3:
            return
        
        if np.random.uniform(0,1) > 0.7:
            if np.random.uniform(0,1) < 0.5:
                head_x = np.random.uniform(30,80)
            else:
                head_x = np.random.uniform(-80,-30)
            head_y = np.random.uniform(-10,10)
            print('head_x:',head_x,'head_y:',head_y)
        
            speed = 0.02
            self.robot.setAngle("head_z",head_x,speed)
            self.robot.setAngle("head_y",head_y,speed)
        else:
            print('waiting')
        
        
