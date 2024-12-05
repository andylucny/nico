from agentspace import Agent, space
import numpy as np
import cv2 as cv
import time

from beeply.notes import beeps
beeper = beeps(250)
def beep():
    beeper.hear("C__")

beep()

from nicomover import enableTorque, disableTorque, setAngle, getAngle, getAngleLowerLimit, getAngleUpperLimit

rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y','r_wrist_z','r_wrist_x','r_indexfinger_x']

def enable():
    global enabled
    enabled = True
    enableTorque(rightArmDofs)

enable()

def disable():
    global enabled
    enabled = False
    disableTorque(rightArmDofs)

def set(angles, angular_speed=0.04):
    for dof, angle in zip(rightArmDofs,angles):
        setAngle(dof,angle,angular_speed)

def setone(dof, angle, angular_speed=0.04):
    setAngle(dof,angle,angular_speed)

def get():
    return [ getAngle(dof) for dof in rightArmDofs ]

poses = []
def save(pose):
    print('append',pose)
    global poses
    poses.append(pose)
    with open('poses.txt','wt') as f:
        f.write(str(rightArmDofs)+'\n')
        for pose in poses:
            f.write(str(pose)+'\n')
    print('saving',len(poses))
    beep()

def getRange(dof):
    low_ = getAngleLowerLimit(dof)
    high_ = getAngleUpperLimit(dof)
    low = min(round(low_,-1),round(high_,-1))
    high = max(round(low_,-1),round(high_,-1))
    defval = getAngle(dof)
    return low, high, defval

class ActionAgent(Agent):

    def init(self):
        space.attach_trigger('whistle',self)

    def senseSelectAct(self):
        whistle = space(default=0)['whistle']
        
        if whistle == 1:
            if not enabled:
                enable()
                print('enabled')
            else:
                disable()
                print('disabled')

        elif whistle == 2:
            if enabled:
                pose = get()
                save(pose)
            else:
                print('not enabled')
