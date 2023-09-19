import numpy as np
import time
from nicomotion.Motion import Motion
import os

def quit():
    try:
        del robot
    except:
        pass
    os._exit(0)

motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

leftArmDofs = ['l_shoulder_z','l_shoulder_y','l_arm_x','l_elbow_y','l_wrist_z','l_wrist_x','l_thumb_z','l_thumb_x','l_indexfinger_x','l_middlefingers_x','head_z','head_y']

def enableTorque():
    for dof in leftArmDofs:
        robot.enableTorque(dof)

def disableTorque():
    for dof in leftArmDofs:
        robot.disableTorque(dof)

enableTorque()

def getLeftArm():
    angles = []
    for dof in leftArmDofs:
        angle = robot.getAngle(dof)
        angles.append(angle)
    return angles

def setLeftArm(angles,duration=2.0):
    for dof,angle in zip(leftArmDofs,angles):
        motor = getattr(robot._robot, dof)
        motor.goto_position(angle,duration=duration,wait=False)

pose0 = [-5.93, 24.13, 22.11, 62.2, 62.29, 40.22, 9.98, 0.04, -180.0, 166.02, 1.1, -1.45] #
# test
# setLeftArm(pose0)
# print(getLeftArm())

posesA = [
    [54.9, 42.42, 15.52, 144.31, 171.65, 0.66, 6.02, 0.04, -180.0, 164.7, -29.85, -20.26],
    [43.12, 36.0, 16.22, 135.16, 169.36, 0.66, 6.02, 0.04, -180.0, 164.7, -20.7, -18.24],
    [43.47, 37.05, 15.52, 132.18, 171.65, 55.6, 1.98, 0.04, -180.0, 163.38, -15.87, -20.44],
    [30.81, 30.9, 15.6, 118.9, 170.59, 117.23, 6.02, 0.04, -180.0, 164.7, -0.92, -26.68],
    [14.29, 25.98, 16.66, 109.58, 171.65, 130.24, 6.02, 0.04, -180.0, 164.7, 2.86, -22.37],
    [11.21, 30.9, 15.96, 115.56, 170.59, 147.91, 6.02, 0.04, -180.0, 166.02, 12.26, -25.1],
    [-0.66, 31.08, 16.22, 118.64, 171.65, 110.55, 6.02, 0.31, -180.0, 164.7, 17.27, -18.33],
    [-5.76, 42.24, 15.87, 139.74, 170.59, 40.22, 6.02, 0.31, -179.91, 164.7, 23.87, -19.3], # out of LCD
]

posesB = [
    [61.85, 31.87, 15.43, 125.93, 170.59, 31.43, 5.67, 0.04, -180.0, 164.0, -36.26, -26.77],
    [49.63, 29.05, 16.04, 114.33, 152.92, 163.56, 5.14, 0.04, -179.91, 164.7, -27.12, -24.57],
    [40.48, 16.84, 13.14, 97.36, 152.48, 165.58, 5.14, 0.04, -180.0, 164.7, -18.59, -29.23],
    [31.6, 10.42, 15.43, 88.4, 154.07, 167.69, 9.98, 0.04, -180.0, 163.38, -4.97, -33.54],
    [17.19, 9.1, 15.25, 87.52000000000001, 152.75, 167.69, 9.98, 0.04, -180.0, 164.7, 11.91, -31.87], 
    [6.73, 10.51, 15.43, 88.75, 154.07, 165.58, 5.67, 0.04, -180.0, 164.7, 18.86, -33.98],
    [-2.95, 16.66, 15.25, 95.25, 163.82, 165.58, 8.04, 0.04, -180.0, 166.02, 13.85, -28.44],
    [-8.57, 20.53, 15.69, 99.82, 171.65, 167.69, 6.02, 0.04, -180.0, 164.7, 30.99, -26.42], # out of LCD
]

posesC = [
    [61.14, 25.54, 15.96, 108.44, 152.75, 172.26, 6.02, 0.04, -180.0, 164.7, -32.84, -30.2],
    [63.25, 10.42, 15.52, 88.4, 154.07, 176.48, 4.0, 0.04, -180.0, 164.7, -30.64, -33.54],
    [58.24, -0.31, 14.29, 77.49000000000001, 151.08, 167.69, 9.98, 0.04, -180.0, 164.7, -23.6, -37.76],
    [46.46, -9.63, 15.69, 67.65, 153.71, 172.09, 9.98, 0.04, -180.0, 163.38, -0.48, -35.12],
    [16.92, -10.86, 16.22, 66.42, 156.0, 176.48, 9.98, 0.04, -180.0, 164.7, 6.55, -30.81],
    [6.46, -13.32, 18.07, 63.870000000000005, 156.0, 176.48, 9.98, 0.04, -180.0, 164.18, 25.19, -32.84],
    [-8.57, -7.78, 23.87, 68.18, 156.0, 176.48, 9.98, 0.04, -180.0, 164.7, 38.02, -33.19],
    [-8.66, -11.12, 38.11, 69.85, 171.65, 136.92, 9.98, 0.04, -180.0, 163.38, 42.24, -36.53], # out of LCD
]

poses = [posesA, posesB, posesC]

def setDefaultPose(speed=0.04):
    allDofs = robot.getJointNames()
    poseBase = [1.19, -35.38, -6.81, -20.35, 33.54, 71.52, -6.81, -20.35, 33.54, 71.52, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0] #
    for dof, angle in zip(allDofs,poseBase):
        robot.setAngle(dof,angle,speed)
    time.sleep(3.0)
    
setDefaultPose()
setLeftArm(pose0)

def touch(p,duration=2.0):
    x = ord(p[1])-ord('1')
    y = ord(p[0])-ord('A')
    pose = poses[y][x]
    points = setLeftArm(pose,duration)
    time.sleep(duration+0.2)
    points = setLeftArm(pose0,duration)
    time.sleep(duration)

def globalTest(duration=2.0):
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7']:
            if f+g == 'A2':
                continue
            touch(f+g,duration)
            time.sleep(1)

#touch('B1')
#globalTest()

from TouchAgent import TouchAgent, stopAllMotors
TouchAgent(robot)
#stopAllMotors(robot)
#setLeftArm(pose0)

time.sleep(2)
globalTest()

