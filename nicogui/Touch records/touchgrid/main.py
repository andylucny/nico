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
    startPose = [-9.0, 45.0, 1.0, 77.0, 59.0, 16.0, 0.0, 32.0, 0.0, 20.0]
    if p[0]=='B' and p[1]=='3': #B3
        middlePose = [19.0, 34.0, 49.0, 111.0, 21.0, 40.0, 0.0, 58.0, 0.0, 81.0]
        endPose = [35.0, 30.0, 49.0, 114.0, 90.0, 40.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0]=='A' and p[1]=='1': #A1
        middlePose = [72.0, 48.0, 15.0, 163.0, 82.0, 1.0, 0.0, 61.0, 17.0, 102.0,]
        endPose = [-9.0, 16.0, 50.0, 112.0, 21.0, 12.0, 0.0, 53.0, 17.0, 101.0]
    elif p[0] == 'A' and p[1] == '2':  # A2
        middlePose = [52.0, 63.0, 33.0, 180.0, 90.0, 6.0, 0.0, 42.0, 0.0, 49.0]
        endPose = [12.0, -3.0, 38.0, 91.0, -1.0, 12.0, 0.0, 39.0, 0.0, 49.0]
    elif p[0] == 'A' and p[1] == '3':  # A3
        middlePose = [62.0, 25.0, 1.0, 130.0, 45.0, 13.0, 0.0, 39.0, 0.0, 48.0]
        endPose = [0.0, 16.0, 43.0, 112.0, 9.0, 10.0, 0.0, 38.0, 0.0, 49.0 ]
    elif p[0] == 'A' and p[1] == '4':  # A4
        middlePose = [16.0, 57.0, 46.0, 144.0, 88.0, 47.0, 0.0, 57.0, 0.0, 54.0]
        endPose = [-9.0, 8.0, 50.0, 102.0, 14.0, 44.0, 0.0, 57.0, 0.0, 53.0]
    elif p[0] == 'A' and p[1] == '5':  # A5
        middlePose = [13.0, 66.0, 36.0, 157.0, 71.0, 12.0, 0.0, 38.0, 0.0, 48.0]
        endPose = [0.0, 8.0, 45.0, 101.0, 17.0, 11.0, 0.0, 32.0, 0.0, 48.0]
    elif p[0] == 'A' and p[1] == '6':  # A6
        middlePose = [49.0, -7.0, -31.0, 125.0, 1.0, 0.0, 0.0, 61.0, 0.0, 51.0]
        endPose = [2.0, 10.0, 39.0, 105.0, 6.0, -3.0, 0.0, 61.0, 0.0, 47.0]
    elif p[0] == 'A' and p[1] == '7':  # A7
        middlePose = [8.0, 37.0, 15.0, 130.0, 60.0, 14.0, 0.0, 59.0, 0.0, 83.0]
        endPose = [-9.0, 10.0, 50.0, 104.0, 7.0, 25.0, 0.0, 59.0, 0.0, 83.0]
    elif p[0] == 'A' and p[1] == '8':  # A8
        middlePose = [2.0, 66.0, 22.0, 180.0, 90.0, 25.0, 0.0, 58.0, 0.0, 83.0]
        endPose = [-9.0, 17.0, 50.0, 110.0, 20.0, 24.0, 0.0, 57.0, 0.0, 83.0]
    elif p[0] == 'B' and p[1] == '1':  # B1
        middlePose = [48.0, 49.0, 48.0, 144.0, 81.0, 26.0, 0.0, 57.0, 0.0, 82.0]
        endPose = [10.0, 6.0, 38.0, 99.0, 11.0, 33.0, 0.0, 58.0, 0.0, 82.0]
    elif p[0] == 'B' and p[1] == '2':  # B2
        middlePose = [78.0, 12.0, -6.0, 122.0, 39.0, 31.0, 0.0, 57.0, 0.0, 82.0]
        endPose = [13.0, 12.0, 22.0, 111.0, -23.0, 26.0, 0.0, 57.0, 0.0, 82.0]
    elif p[0] == 'B' and p[1] == '4':  # B4
        middlePose = [22.0, 28.0, 49.0, 106.0, 82.0, 44.0, 0.0, 57.0, 0.0, 81.0]
        endPose = [11.0, 10.0, 22.0, 107.0, -17.0, 42.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'B' and p[1] == '5':  # B5
        middlePose = [24.0, 10.0, 21.0, 100.0, 58.0, 42.0, 0.0, 57.0, 0.0, 82.0]
        endPose = [4.0, 7.0, 21.0, 104.0, -22.0, 41.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'B' and p[1] == '6':  # B6
        middlePose = [12.0, 13.0, 19.0, 102.0, 67.0, 47.0, 0.0, 57.0, 0.0, 81.0]
        endPose = [-5.0, 12.0, 19.0, 110.0, -16.0, 47.0, 0.0, 58.0, 0.0, 81.0]
    elif p[0] == 'B' and p[1] == '7':  # B7
        middlePose = [1.0, 20.0, 21.0, 110.0, 77.0, 47.0, 0.0, 58.0, 0.0, 81.0]
        endPose = [-4.0, 16.0, 21.0, 110.0, -5.0, 46.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'B' and p[1] == '8':  # B8
        middlePose = [-3.0, 24.0, 13.0, 122.0, 54.0, 37.0, 0.0, 58.0, 0.0, 82.0]
        endPose = [-9.0, 12.0, 24.0, 109.0, -16.0, 38.0, 0.0, 59.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '1':  # C1
        middlePose = [65.0, 37.0, 40.0, 132.0, 74.0, 40.0, 0.0, 57.0, 0.0, 81.0]
        endPose = [-9.0, 10.0, 50.0, 105.0, 2.0, 47.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '2':  # C2
        middlePose = [46.0, 25.0, 50.0, 104.0, 72.0, 48.0, 0.0, 57.0, 0.0, 81.0]
        endPose = [7.0, 23.0, 33.0, 114.0, -10.0, 44.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '3':  # C3
        middlePose = [45.0, 2.0, 43.0, 88.0, 85.0, 42.0, 0.0, 57.0, 0.0, 82.0]
        endPose = [-3.0, 8.0, 26.0, 104.0, -6.0, 35.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '4':  # C4
        middlePose = [26.0, 5.0, 37.0, 73.0, 68.0, 35.0, 0.0, 57.0, 0.0, 81.0]
        endPose = [-6.0, 6.0, 38.0, 100.0, -3.0, 33.0, 0.0, 57.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '5':  # C5
        middlePose = [16.0, -13.0, 40.0, 78.0, 89.0, 23.0, 0.0, 47.0, 0.0, 82.0]
        endPose = [-8.0, -1.0, 36.0, 93.0, 0.0, 25.0, 0.0, 45.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '6':  # C6
        middlePose = [1.0, -12.0, 37.0, 70.0, 85.0, 25.0, 0.0, 46.0, 0.0, 81.0]
        endPose = [-6.0, 10.0, 21.0, 108.0, -17.0, 23.0, 0.0, 32.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '7':  # C7
        middlePose = [-4.0, 12.0, 39.0, 102.0, -5.0, 22.0, 0.0, 33.0, 0.0, 81.0]
        endPose = [-9.0, 6.0, 31.0, 101.0, -7.0, 39.0, 0.0, 32.0, 0.0, 81.0]
    elif p[0] == 'C' and p[1] == '8':  # C8
        middlePose = [-9.0, -1.0, 14.0, 96.0, 51.0, 21.0, 0.0, 32.0, 0.0, 80.0]
        endPose = [-9.0, 5.0, 42.0, 99.0, -4.0, 24.0, 0.0, 32.0, 0.0, 80.0]
    else:
        print("try again")
    perform([startPose,middlePose,endPose])
    time.sleep(1.0)
    perform([startPose])
    #setDefaultPose()

def globalTest():
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7','8']:
            touch(f+g)
            time.sleep(1.2)

#touch('B7')
#globalTest()
