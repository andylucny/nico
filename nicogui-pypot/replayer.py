import numpy as np
import time

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
        motor = getattr(robot, dof)
		motot.goto_position(angle,duration=duration,wait=False)

pose0 = [-6.0, 26.0, 22.0, 63.0, 34.0, 22.0, 90.0, 95.0, 0.0, 173.0, -2.0, 0.0]
# test
# setLeftArm(pose0)

posesA = [
    [62.0, 54.0, 32.0, 156.0, 90.0, 13.0, 90.0, 93.0, 0.0, 173.0, -22.0, 36.0],
    [56.0, 50.0, 32.0, 154.0, 90.0, 13.0, 90.0, 93.0, 0.0, 173.0, -24.0, 27.0],
    [47.0, 44.0, 32.0, 139.0, 90.0, 27.0, 90.0, 91.0, 0.0, 173.0, -25.0, 19.0],
    [35.0, 38.0, 33.0, 128.0, 90.0, 40.0, 90.0, 93.0, 0.0, 173.0, -26.0, 3.0],
    [24.0, 36.0, 33.0, 124.0, 90.0, 43.0, 90.0, 93.0, 0.0, 173.0, -27.0, -2.0],
    [12.0, 38.0, 33.0, 126.0, 90.0, 47.0, 91.0, 93.0, 0.0, 173.0, -26.0, -14.0],
    [ 3.0, 43.0, 33.0, 136.0, 90.0, 38.0, 91.0, 93.0, 0.0, 173.0, -24.0, -24.0],
    [-6.0, 52.0, 33.0, 154.0, 90.0, 22.0, 91.0, 93.0, 0.0, 173.0, -23.0, -32.0]
]

posesB = [
    [69.0, 40.0, 32.0, 137.0, 90.0, 20.0, 90.0, 95.0, 0.0, 172.0, -28.0, 42.0],
    [60.0, 36.0, 32.0, 125.0, 81.0, 51.0, 90.0, 95.0, 0.0, 173.0, -30.0, 35.0],
    [49.0, 22.0, 32.0, 105.0, 81.0, 51.0, 90.0, 95.0, 0.0, 173.0, -33.0, 23.0],
    [38.0, 11.0, 32.0,  91.0, 81.0, 51.0, 90.0, 95.0, 0.0, 173.0, -35.0, 9.0],
    [23.0, 10.0, 32.0,  90.0, 81.0, 51.0, 90.0, 95.0, 0.0, 173.0, -36.0, -13.0],
    [ 8.0, 11.0, 32.0,  92.0, 81.0, 51.0, 90.0, 95.0, 0.0, 173.0, -34.0, -19.0],
    [-3.0, 16.0, 31.0,  96.0, 86.0, 51.0, 90.0, 94.0, 0.0, 173.0, -31.0, -16.0],
    [-9.0, 26.0, 29.0, 109.0, 90.0, 51.0, 90.0, 93.0, 0.0, 173.0, -28.0, -39.0]
]

posesC = [
    [77.0,  34.0, 32.0, 119.0, 81.0, 53.0, 90.0, 93.0, 0.0, 173.0, -35.0, 42.0],
    [70.0,  12.0, 32.0,  91.0, 81.0, 53.0, 90.0, 94.0, 0.0, 173.0, -35.0, 40.0],
    [59.0,  -1.0, 32.0,  78.0, 81.0, 51.0, 90.0, 95.0, 0.0, 173.0, -36.0, 27.0],
    [47.0, -13.0, 32.0,  67.0, 82.0, 52.0, 90.0, 95.0, 0.0, 173.0, -36.0, 2.0],
    [25.0, -16.0, 32.0,  67.0, 82.0, 53.0, 90.0, 95.0, 0.0, 173.0, -36.0, -7.0],
    [ 7.0, -17.0, 26.0,  63.0, 82.0, 53.0, 90.0, 95.0, 0.0, 173.0, -36.0, -27.0],
    [-9.0, -10.0, 18.0,  69.0, 82.0, 53.0, 90.0, 95.0, 0.0, 173.0, -35.0, -41.0],
    [-9.0, -10.0,  0.0,  75.0, 90.0, 44.0, 90.0, 95.0, 0.0, 173.0, -35.0, -46.0]
]

poses = [posesA, posesB, posesC]

def setDefaultPose(speed=0.04):
    allDofs = robot.getJointNames()
    poseBase = [-7.0, -20.0, 8.0, 73.0, -36.0, 50.0, 65.0, 82.0, 0.0, 0.0, -8.0, -21.0, 8.0, 72.0, -35.0, 50.0, 65.0, 81.0, 0.0, 0.0, -34.0, 0.0]
    for dof, angle in zip(allDofs,poseBase):
        robot.setAngle(dof,angle,speed)
    time.sleep(3.0)
    
setDefaultPose()

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
