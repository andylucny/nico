from nicomotors import NicoMotors
import numpy as np
import time

motors = NicoMotors()
motors.open()
leftArmDofs = ['left-arm1', 'left-arm2', 'left-arm3', 'left-elbow1', 'left-wrist1', 'left-wrist2', 'left-thumb1', 'left-thumb2', 'left-forefinger', 'left-littlefingers']

for dof in leftArmDofs:
	motors.enableTorque(dof)

def setLeftArm(angles):
	for dof,angle in zip(leftArmDofs,angles):
		motors.setPositionDg(dof,angle)

# test
# angles = [-9.0, 48.0, 1.0, 77.0, 58.0, 16.0, 0.0, 32.0, 0.0, 20.0]
# setLeftArm(angles)

def setDefaultPose():
    allDofs = ['left-arm1', 'left-arm2', 'left-arm3', 'left-elbow1', 'left-wrist1', 'left-wrist2', 'left-thumb1', 'left-thumb2', 'left-forefinger', 'left-littlefingers', 'right-arm1', 'right-arm2', 'right-arm3', 'right-elbow1', 'right-wrist1', 'right-wrist2', 'right-thumb1', 'right-thumb2', 'right-forefinger', 'right-littlefingers', 'neck1', 'neck2']
    angles = [21.0, -18.0, 38.0, 77.0, -12.0, 53.0, 0.0, 22.0, 0.0, 0.0, 9.0, -18.0, 41.0, 74.0, -3.0, 50.0, 0.0, 2.0, 0.0, 0.0, -33.0, -2.0]
    for dof, angle in zip(allDofs,angles):
        motors.setPositionDg(dof,angle)
    time.sleep(3.0)
    
setDefaultPose()

def perform(points):
    i = 0
    print('point',i)
    setLeftArm(points[i])
    while i < len(points):
        time.sleep(0.05)
        angles = []
        for dof in leftArmDofs:
            angle = motors.getPositionDg(dof)
            angles.append(angle)
        goal = points[i]
        error = np.linalg.norm(np.array(angles)-np.array(goal))/len(angles)
        print(' error',error)
        eps = 1.0
        if error < eps:
            i += 1
            if i < len(points):
                print('point',i)
                setLeftArm(points[i])
            else:
                print('done')
            
def touch(p):
    print('grid cell:',ord(p[0])-ord('A'), ord(p[1])-ord('1'))
    startPose = [-9.0, 45.0, 1.0, 77.0, 59.0, 16.0, 0.0, 32.0, 0.0, 20.0]
    middlePose = [19.0, 34.0, 49.0, 111.0, 21.0, 40.0, 0.0, 58.0, 0.0, 81.0]
    endPose = [35.0, 30.0, 49.0, 114.0, 90.0, 40.0, 0.0, 57.0, 0.0, 81.0]
    perform([startPose,middlePose,endPose])
    time.sleep(1.0)
    perform([startPose])
    setDefaultPose()

touch('B3')
