from nicomotors import NicoMotors
import numpy as np
import time

motors = NicoMotors()
dofs = motors.dofs()
motors.open()

leftArmDofs = ['left-arm1', 'left-arm2', 'left-arm3', 'left-elbow1', 'left-wrist1', 'left-wrist2', 'left-thumb1', 'left-thumb2', 'left-forefinger', 'left-littlefingers', 'neck1', 'neck2' ]

def enableTorque():
    for dof in leftArmDofs:
        motors.enableTorque(dof)

def disableTorque():
    for dof in leftArmDofs:
        motors.disableTorque(dof)

enableTorque()

def getLeftArm():
    angles = []
    for dof in leftArmDofs:
        angle = motors.getPositionDg(dof)
        angles.append(angle)
    return angles

def setLeftArm(angles):
	for dof,angle in zip(leftArmDofs,angles):
		motors.setPositionDg(dof,angle)

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

def setDefaultPose():
    allDofs = ['left-arm1', 'left-arm2', 'left-arm3', 'left-elbow1', 'left-wrist1', 'left-wrist2', 'left-thumb1', 'left-thumb2', 'left-forefinger', 'left-littlefingers', 'right-arm1', 'right-arm2', 'right-arm3', 'right-elbow1', 'right-wrist1', 'right-wrist2', 'right-thumb1', 'right-thumb2', 'right-forefinger', 'right-littlefingers', 'neck1', 'neck2']
    poseBase = [-7.0, -20.0, 8.0, 73.0, -36.0, 50.0, 65.0, 82.0, 0.0, 0.0, -8.0, -21.0, 8.0, 72.0, -35.0, 50.0, 65.0, 81.0, 0.0, 0.0, -34.0, 0.0]
    for dof, angle in zip(allDofs,poseBase):
        motors.setPositionDg(dof,angle)
    time.sleep(3.0)
    
setDefaultPose()

def perform(points):
    i = 0
    print('point',i)
    setLeftArm(points[i])
    last_error = 1e5
    while i < len(points):
        time.sleep(0.05)
        angles = []
        for dof in leftArmDofs:
            angle = motors.getPositionDg(dof)
            angles.append(angle)
        goal = points[i]
        error = np.linalg.norm(np.array(angles)-np.array(goal))/len(angles)
        print(' error',error)
        eps=3.0 #1.3
        if error < eps:
            if error+0.001 >= last_error:
                i += 1
                if i < len(points):
                    print('point',i)
                    setLeftArm(points[i])
                else:
                    print('done')
        last_error = error

perform([pose0])

def bioforward(pose,w=0.8):
    ps = getLeftArm()
    return [ [w*pose[0]+(1.0-w)*ps[0]]+ps[1:-2]+pose[-2:], pose ]

def biobackward(pose,w=0.0):
    ps = getLeftArm()
    return [ [w*pose[0]+(1.0-w)*ps[0]]+pose[1:], pose ]

def touch(p,w=0.8):
    x = ord(p[1])-ord('1')
    y = ord(p[0])-ord('A')
    pose = poses[y][x]
    #perform([pose0])
    points = bioforward(pose,w)
    perform(points)
    time.sleep(1)
    points = biobackward(pose0)
    perform(points)

def globalTest(w=0.8):
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7','8']:
            if f+g == 'A1':
                continue
            touch(f+g,w)
            time.sleep(1)

#touch('B1')
#globalTest(w=0.8)

"""
def loadRecording(filename):
    recorded = []
    recorded_images = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            r = eval(line[:-1])
            recorded.append(r)
    return recorded, recorded_images
    
#points, _ = loadRecording('fb3.txt')

def predict_blind(points, timeout=1.0):
    for point in points:
        setLeftArm(point)
        time.sleep(timeout)
        
#predict_blind(points,0.5):
        
def measure(points):
    durations = []
    i = 0
    print('point',i)
    setLeftArm(points[i])
    t0 = time.time()
    while i < len(points):
        time.sleep(0.05)
        angles = []
        for dof in leftArmDofs:
            angle = motors.getPositionDg(dof)
            angles.append(angle)
        goal = points[i]
        error = np.linalg.norm(np.array(angles)-np.array(goal))/len(angles)
        print(' error',error)
        eps2 = 1.5
        if error < eps2:
            t1 = time.time()
            duration = t1-t0
            t0 = t1
            durations.append(duration)
            i += 1
            if i < len(points):
                print('point',i)
                setLeftArm(points[i])
            else:
                print('done')
    return durations
    
#ts = measure(points)
#ts = [1.21, 1.20, 0.43, 3.10, 1.90] 

def predict(points, ts, coef=1.0):
    for point, t in zip(points, ts):
        setLeftArm(point)
        time.sleep(t*coef)

#predict(points, ts, 0.95)
"""