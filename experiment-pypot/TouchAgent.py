from agentspace import Agent, space
import numpy as np
import cv2 as cv
import os
import time
import pyautogui

def stopAllMotors(_robot):
    for motor in _robot._robot.motors:
        motor.goal_position = motor.present_position

class TouchAgent(Agent):

    def __init__(self, robot):
        self.robot = robot
        super().__init__()
        
    def mouseHandler(self, event, x, y, flags, param):
        radius = 15
        if event == cv.EVENT_LBUTTONDOWN:
            pass
            #cv.circle(self.screen,(x,y),radius,(0,255,0),cv.FILLED)
        elif event == cv.EVENT_LBUTTONUP:
            cv.circle(self.screen,(x,y),radius,(0,0,255),cv.FILLED)
        else:
            pass
            #cv.circle(self.screen,(x,y),radius,(0,255,0),cv.FILLED)
        self.touch = True
        
    def init(self):

        width, height = pyautogui.size()
        cv.namedWindow("image",cv.WINDOW_NORMAL)
        cv.setMouseCallback("image", self.mouseHandler)
        self.screen = np.zeros((height,width,3),np.uint8)
        self.touch = False
        self.mouse = pyautogui.position()

        while True:
            if self.touch:
                pyautogui.moveTo(self.mouse[0], self.mouse[1])
                #pyautogui.drag(0,0,0.1,button='left')
                self.touch = False
            else:
                mouse = pyautogui.position()
                if mouse[0] < width:
                    self.mouse = mouse
            cv.imshow("image", self.screen)
            key = cv.waitKey(10)
            if key == 27:
                break
            elif key == 's':
                stopAllMotors(self.robot)

        cv.destroyAllWindows()
        
    def senseSelectAct(self):
        pass
    
if __name__ == "__main__":

    from nicomotion.Motion import Motion
    motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
    robot = Motion(motorConfig=motorConfig)
    
    TouchAgent(robot)
    motor = robot._robot.motors[0]
    #motor.goto_position(50,duration=20,wait=False)
    