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
    [61.58, 49.71, 13.58, 154.51, 171.65, 0.66, 6.02, 0.04, -180.0, 166.02, -32.4, -22.73], #
    [55.69, 46.37, 13.49, 152.13, 170.42, 0.66, 6.02, 0.04, -180.0, 166.02, -23.96, -24.75], #
    [46.73, 41.27, 13.49, 137.54, 171.65, 62.2, 1.98, 0.04, -180.0, 164.7, -16.31, -25.89], #
    [34.77, 35.47, 12.53, 126.29, 171.65, 117.23, 6.02, 0.04, -180.0, 164.7, -1.19, -26.95], #
    [23.96, 33.45, 12.7, 122.33, 171.65, 130.24, 6.02, 0.04, -180.0, 166.02, 3.12, -28.0], #
    [11.91, 35.47, 12.7, 124.26, 170.59, 147.91, 6.02, 1.98, -180.0, 166.02, 14.46, -26.95], #
    [2.86, 40.22, 12.7, 134.02, 171.65, 110.55, 6.02, 1.98, -180.0, 164.7, 23.87, -24.75], #
    [-5.85, 48.84, 12.7, 152.13, 171.65, 40.22, 6.02, 1.98, -179.91, 166.02, 31.43, -23.6] #
]

posesB = [
    [68.7, 36.88, 13.58, 135.34, 170.59, 31.43, 9.98, 0.04, -180.0, 164.0, -38.02, -29.14], #
    [59.74, 33.8, 13.49, 122.95, 152.92, 165.58, 9.98, 0.04, -179.91, 166.02, -31.43, -31.16], #
    [48.84, 20.62, 13.49, 103.52, 154.07, 165.58, 9.98, 0.04, -180.0, 166.02, -20.0, -34.42], #
    [37.76, 10.07, 13.49, 89.54, 154.07, 167.69, 9.98, 0.04, -180.0, 166.02, -6.9, -36.7], #
    [22.9, 9.01, 13.58, 88.48, 154.07, 167.69, 9.98, 0.04, -180.0, 166.02, 13.49, -37.67], #
    [7.78, 10.07, 13.49, 90.33, 154.07, 165.58, 9.98, 0.04, -180.0, 164.7, 19.21, -35.56], #
    [-3.12, 14.99, 14.37, 94.46, 163.82, 167.69, 8.04, 0.04, -180.0, 166.02, 16.31, -32.4], #
    [-8.75, 23.6, 16.04, 107.21, 171.65, 167.69, 6.02, 0.04, -180.0, 166.02, 38.02, -29.14] #
]

posesC = [
    [76.44, 31.16, 13.58, 117.23, 152.75, 176.48, 6.02, 0.04, -180.0, 166.02, -38.11, -36.62], #
    [69.76, 11.12, 13.49, 89.54, 154.07, 176.48, 8.04, 0.04, -180.0, 164.7, -36.09, -36.62], #
    [58.77, -1.63, 13.58, 76.62, 154.07, 167.69, 9.98, 0.04, -180.0, 166.02, -23.87, -37.67], #
    [46.81, -13.32, 13.49, 66.24, 156.0, 172.09, 9.98, 0.04, -180.0, 164.7, -0.66, -37.76], #
    [24.75, -15.69, 13.58, 65.54, 156.0, 176.48, 9.98, 0.04, -180.0, 164.7, 7.78, -37.76], #
    [7.08, -17.27, 18.59, 62.29, 156.0, 176.48, 9.98, 0.04, -180.0, 166.02, 26.77, -37.76], #
    [-8.75, -10.42, 25.27, 67.47, 156.0, 176.48, 9.98, 0.04, -180.0, 164.7, 39.87, -36.62], #
    [-8.75, -10.51, 40.4, 73.54, 171.65, 136.92, 9.98, 0.04, -180.0, 164.7, 44.62, -36.62] #
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
    time.sleep(duration+2.0)
    points = setLeftArm(pose0,duration)
    time.sleep(duration)

def globalTest(duration=2.0):
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7','8']:
            if f+g == 'A1':
                continue
            touch(f+g,duration)
            time.sleep(1)

#touch('B1')
#globalTest()

