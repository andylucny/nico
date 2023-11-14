import os

from nico.agentspace import Agent, space, Trigger

from nico.CameraAgent import CameraAgent
from nico.PerceptionAgent import PerceptionAgent
from nico.FaceAgent import FaceAgent
from nico.ActionAgent import ActionAgent
from nico.ControlAgent import ControlAgent
from nico.ViewerAgent import ViewerAgent
from nico.RandomAgent import RandomAgent

from nico.download import download_all
download_all()

from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
try:
    robot = Motion(motorConfig=motorConfig)
except:
    print('motors are simulated')
    from nico.nicodummy import DummyRobot
    robot = DummyRobot()

import signal
import time

def shutdown():
    Agent.stopAll()
    try:
        del robot
    except:
        pass

def quit():
    shutdown()
    os._exit(0)
    
# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

def enableTorque():
    allDofs = robot.getJointNames()
    for dof in allDofs:
        robot.enableTorque(dof)

def disableTorque():
    allDofs = robot.getJointNames()
    for dof in allDofs:
        robot.disableTorque(dof)

def setDefaultPose(speed=0.04):
    allDofs = robot.getJointNames()
    poseBase = [1.19, -35.38, -6.81, -20.35, 33.54, 71.52, -6.81, -20.35, 33.54, 71.52, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0] #
    for dof, angle in zip(allDofs,poseBase):
        robot.setAngle(dof,angle,speed)
    time.sleep(3.0)

def startup():
    enableTorque()
    righteye = CameraAgent('See3CAM_CU135',0,'camera',fps=10,zoom=350) # right eye
    time.sleep(1)
    dummy = righteye.stopped
    if dummy:
        camera = CameraAgent('',0,'camera')
    else:
        lefteye = CameraAgent('See3CAM_CU135',1,'wide camera',fps=10,zoom=170) # left eye
    time.sleep(1)
    PerceptionAgent('camera','features','points','point2') # dino model pointing to 6 points, one preferred 
    time.sleep(1)
    FaceAgent('camera' if dummy else 'wide camera','face position','face','emotion','face point') # face detector
    time.sleep(1)
    ActionAgent(robot,'point') # turn to shown objects
    time.sleep(1)
    ControlAgent('points','face point','point',followCloseObjects=False) # point selection 
    time.sleep(1)
    RandomAgent(robot)
    time.sleep(1)
    ViewerAgent('camera','wide camera','points','face point','point') # view image from camera

def setmode(mode): # 0 .. look to the touchscreen, 1 .. look to face, 2 .. look around, 3 .. random look
    space['mode'] = mode
    if mode == 0:
        space['point'] = None
        robot.setAngle("head_z",0.0,0.05)
        robot.setAngle("head_y",-40.0,0.05)
    elif mode == 3:
        space['point'] = None
        robot.setAngle("head_z",50.0,0.02)
        robot.setAngle("head_y",30.0,0.02)

if __name__ == "__main__":

    startup()
    print('looking on touchscreen')
    setmode(0)
    time.sleep(20)
    print('looking on face')
    setmode(1)
    time.sleep(20)
    print('looking around')
    setmode(2)
    time.sleep(20)
    shutdown()
