pose0 = [-5.93, 24.13, 22.11, 62.2, 62.29, 40.22, 9.98, 0.04, -180.0, 166.02, 1.1, -1.45] #

posesA = [
    [49.44, 44.36, 10.41, 129, 150.1, 159.78, 0.3, 0.04, -180.0, 165.4, -23, -28],
    [40.96, 38.55, 11.56, 123.2, 153.14, 139.83, -4.0, 0.04, -180.0, 161.45, -16, -28],
    [32.49, 32.74, 12.7, 118.46, 156.17, 119.88, -8.3, 0.04, -180.0, 157.5, -6, -29],
    [24.57, 32.99, 12.66, 116.64, 154.83, 129.68, -6.28, 0.04, -180.0, 160.6, 0, -29],
    [20.53, 23.69, 15.52, 112, 158.99, 85.67, -12.62, 0.04, -180.0, 153.54, 7, -29],
    [8.18, 27.43, 13.76, 110.07, 156.52, 119.52, -8.57, 0.04, -180.0, 159.74, 19, -29],
    [-4.18, 31.17, 12.01, 110.03, 154.06, 153.36, -4.53, 0.04, -180.0, 165.93, 30, -29]
]

posesB = [
    [56.58, 31.68, 13.76, 112, 155.12, 150.02, -9.36, 0.04, -180.0, 157.41, -29, -33],
    [47.87, 21.58, 14.11, 103.43, 155.12, 148.18, -2.15, 0.04, -180.0, 161.1, -18, -32],
    [40.48, 16.84, 13.14, 99, 152.48, 165.58, 5.14, 0.04, -180.0, 164.7, -18.59, -29.23],
    [31.6, 10.42, 15.43, 88.4, 154.07, 167.69, 9.98, 0.04, -180.0, 163.38, -4.97, -33.54],
    [17.19, 9.1, 15.25, 87.52, 152.75, 167.69, 9.98, 0.04, -180.0, 164.7, 11.91, -31.87], 
    [6.73, 10.51, 15.43, 88.75, 154.07, 165.58, 5.67, 0.04, -180.0, 164.7, 18.86, -33.98],
    [-4.53, 12.09, 15.52, 90.50999999999999, 155.38, 157.14, 1.36, 0.04, -180.0, 164.7, 25.45, -36.09]
]

posesC = [
    [63.25, 10.42, 15.52, 88.4, 154.07, 176.48, 4.0, 0.04, -180.0, 164.7, -30.64, -33.54],
    [58.24, -0.31, 14.29, 77.49, 151.08, 167.69, 9.98, 0.04, -180.0, 164.7, -23.6, -37.76],
    [46.46, -9.63, 15.69, 67.65, 153.71, 172.09, 9.98, 0.04, -180.0, 163.38, -13, -35.12],
    [31.52, -10.68, 15.87, 66.77, 154.86, 171.38, 9.98, 0.04, -180.0, 164.0, 2.68, -32.84],
    [16.92, -10.86, 16.22, 66.42, 156.0, 176.48, 9.98, 0.04, -180.0, 164.7, 16, -30.81],
    [6.46, -13.32, 18.07, 65, 156.0, 176.48, 9.98, 0.04, -180.0, 164.18, 25.19, -32.84],
    [-4.88, -6.99, 19.03, 70.99, 156.7, 160.92, 7.25, 0.04, -180.0, 163.47, 34.77, -32.04]
]

poses = [posesA, posesB, posesC]

"""
with open('pom.txt','wt') as file:
    file.write("['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x', 'l_thumb_z', 'l_thumb_x', 'l_indexfinger_x', 'l_middlefingers_x', 'head_z', 'head_y']\n")
    file.write(str(pose0)+'\n')
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7']:
            if f+g == 'A2':
                continue
            p = f+g
            x = ord(p[1])-ord('1')
            y = ord(p[0])-ord('A')
            pose = poses[y][x]
            file.write(str(pose)+'\n')
            file.write(str(pose0)+'\n')
"""

import time
import numpy as np
from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

import os
def quit():
    try:
        del robot
    except:
        pass
    os._exit(0)

leftArmDofs = ['l_shoulder_z','l_shoulder_y','l_arm_x','l_elbow_y','l_wrist_z','l_wrist_x','l_thumb_z','l_thumb_x','l_indexfinger_x','l_middlefingers_x','head_z','head_y']
rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y','r_wrist_z','r_wrist_x','r_thumb_z','r_thumb_x','r_indexfinger_x','r_middlefingers_x','head_z','head_y']

def enableTorque():
    for dof in leftArmDofs:
        robot.enableTorque(dof)
    for dof in rightArmDofs:
        robot.enableTorque(dof)

def disableTorque():
    for dof in leftArmDofs:
        robot.disableTorque(dof)
    for dof in rightArmDofs:
        robot.disableTorque(dof)

enableTorque()

def getLeftArm():
    angles = []
    for dof in leftArmDofs:
        angle = robot.getAngle(dof)
        angles.append(angle)
    return angles

def getRightArm():
    angles = []
    for dof in rightArmDofs:
        angle = robot.getAngle(dof)
        angles.append(angle)
    return angles

def setLeftArm(angles,duration=2.0):
    for dof,angle in zip(leftArmDofs,angles):
        motor = getattr(robot._robot, dof)
        motor.goto_position(angle,duration=duration,wait=False)

def setRightArm(angles,duration=2.0):
    for dof,angle in zip(rightArmDofs,angles):
        motor = getattr(robot._robot, dof)
        motor.goto_position(angle,duration=duration,wait=False)

def touch(p,duration=2.0):
    if isinstance(p,list):
        poseis = []
        for pi in p:
            x = ord(pi[1])-ord('1')
            y = ord(pi[0])-ord('A')
            posei = poses[y][x]
            poseis.append(posei)
        pose = np.average(poseis,axis=0)
    else:
        x = ord(p[1])-ord('1')
        y = ord(p[0])-ord('A')
        pose = poses[y][x]
    setLeftArm(pose,duration)
    time.sleep(duration+1.0) 
    setLeftArm(pose0,duration)
    time.sleep(duration)
    
def touchPose(pose,duration=2.0):
    setLeftArm(pose,duration)
    time.sleep(duration+1.0) 
    setLeftArm(pose0,duration)
    time.sleep(duration)

samples = ['B3','B4','B5','B6','B7','C2','C3','C4','C5','C6']

def getPose(p):
    x = ord(p[1])-ord('1')
    y = ord(p[0])-ord('A')
    pose = poses[y][x]
    return np.array(pose)

def stopAllMotors():
    for motor in robot._robot.motors:
        motor.goal_position = motor.present_position

from TouchAgent import TouchAgent, clean
TouchAgent()

from agentspace import Agent, space, Trigger

class StoppingAgent(Agent):
    def init(self):
        space.attach_trigger("touch",self,Trigger.NAMES)
    def senseSelectAct(self):
        #print('stopping motors')
        stopAllMotors()
        #print('recording')
        #print(space["touch"])
        angles = getRightArm()
        print('***',angles[0],angles[1],angles[3],'***',space["touch"])

stopper = StoppingAgent()

c1 = getPose('C1')
c2 = getPose('C2')
c3 = getPose('C3')
c4 = getPose('C4')
c5 = getPose('C5')
c6 = getPose('C6')
c7 = getPose('C7')

b1 = getPose('B1')
b2 = getPose('B2')
b3 = getPose('B3')
b4 = getPose('B4')
b5 = getPose('B5')
b6 = getPose('B6')
b7 = getPose('B7')

a1 = getPose('A1')
a2 = getPose('A2')
a3 = getPose('A3')
a4 = getPose('A4')
a5 = getPose('A5')
a6 = getPose('A6')
a7 = getPose('A7')

#a3 = 2*b3-c3
#touchPose(a3)
#aa3 = [14.55, 23.69, 15.43, 105.8, 151.08, 150.55, 0.31, 0.04, -180.0, 159.52, -9.01, -15.69]
#touchPose(aa3)

#a2 = 2*b3-c4
#touchPose(a2)
#aa2 = [18.33, 30.55, 14.2, 108.18, 153.89, 163.47, 0.31, 0.04, -180.0, 163.38, -11.12, -16.4]
#touchPose(aa2)

#bb=np.array([53.76, 21.49, 12.88, 101.41, 153.27, 159.78, 0.31, 0.04, -180.0, 161.8, -40.48, -22.55])
#aa=np.array([49.27, 38.64, 12.0, 125.93, 155.47, 151.87, -9.36, 0.04, -180.0, 158.9, -56.92, -6.9])
#a2=np.array([40.22, 32.66, 14.02, 116.78999999999999, 156.7, 147.03, -9.36, 0.04, -180.0, 158.9, -47.25, -4.7])
#a3=np.array([34.33, 28.0, 16.04, 109.67, 156.7, 145.01, -9.36, 0.04, -180.0, 158.9, -40.4, -3.65])
#a4=np.array([31.6, 24.31, 16.84, 107.3, 156.7, 140.09, -9.36, 0.04, -180.0, 158.9, -37.93, -2.68])
#bc=np.array([43.3, 27.03, 14.02, 106.68, 154.33, 155.82, -4.53, 0.04, -180.0, 160.31, -40.92, -11.91])

#b2=[48.53, 24.26, 13.45, 104.045, 153.8, 157.8, -2.11, 0.04, -180.0, 161.055, -40.7, -17.23]

def lst(x):
    return list(np.round(100*x)/100.0)

#b1=np.array([56.58, 31.68, 13.76, 110.73, 155.12, 150.02, -9.36, 0.04, -180.0, 157.41, -62.81, -5.23])

#a3=np.array([32.49, 32.74, 12.7, 118.46, 156.17, 119.88, -8.3, 0.04, -180.0, 157.5, -48.04, 1.1])
#a1=np.array([49.44, 44.36, 10.41, 127.95, 150.1, 159.78, 0.3, 0.04, -180.0, 165.4, -39.86, -25.62])
#a2=np.array([40.96, 38.55, 11.56, 123.2, 153.14, 139.83, -4.0, 0.04, -180.0, 161.45, -43.95, -12.26])
#a5=np.array([20.53, 23.69, 15.52, 110.11, 158.99, 85.67, -12.62, 0.04, -180.0, 153.54, -47.08, 11.74])
#a7=np.array([-4.18, 31.17, 12.01, 110.03, 154.06, 153.36, -4.53, 0.04, -180.0, 165.93, 16.13, -40.14])
#a6=np.array([8.18, 27.43, 13.76, 110.07, 156.52, 119.52, -8.57, 0.04, -180.0, 159.74, -15.48, -14.2])
#a4=np.array([24.57, 32.99, 12.66, 116.64, 154.83, 129.68, -6.28, 0.04, -180.0, 160.6, -29.72, -13.23])

# head

touchesA = [
    (2064, 462),
    (1675, 285),
    (1369, 223),
    (1079, 215),
    (881, 233),
    (556, 310),
    (195, 454)
]

touchesB = [
    (2100, 645),
    (1794, 568),
    (1596, 559),
    (1247, 603),
    (849, 588),
    (554, 617),
    (240, 697)
]

touchesC = [
    (2040, 999),
    (1827, 1089),
    (1474, 1087),
    (1166, 1009),
    (857, 1001),
    (619, 1073),
    (344, 1032)
]

touches = [ touchesA, touchesB, touchesC ]

def displayPose(p):
    x = ord(p[1])-ord('1')
    y = ord(p[0])-ord('A')
    touch = touches[y][x]
    space['ShowIntention'] = True
    space['emulated'] = (2400 - touch[0],touch[1])

#setRightArm(pose0)
#displayPose('A1')
#setRightArm(a1)

arm1 = 40.0
arm2 = 50.0
elbow = 90.0

def get():
    pos = getRightArm()
    print(pos)
    return pos

def set():
    global arm1, arm2, elbow
    a = [arm1, arm2, 24.0, elbow, 155.0, 140.0, -120.0, 0.0, -150.0, 180.0,]
    setRightArm(a)

set()

"""
def calculate(d):
    l = np.sqrt(d**2+22**2)
    fi = 20.15*np.pi/180
    np.arctan(d/22)
"""

def measure(arm2_):
    global arm1, arm2, elbow
    arm2 = arm2_
    elbow = 80
    set()
    time.sleep(3)
    elbow = 180
    set()
    time.sleep(3)
    elbow = 80
    set()
