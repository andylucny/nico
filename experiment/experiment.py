from nicomotors import NicoMotors
import PySimpleGUI as sg
from agentspace import Agent, space
import numpy as np
import time, random

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

pose0 = [-6.0, 26.0, 22.0, 63.0, 34.0, 22.0, 90.0, 95.0, 0.0, 173.0, -2.0, 0.0] # priprava na ukazanie
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
    #print('point',i)
    setLeftArm(points[i])
    while i < len(points):
        time.sleep(0.05)
        if space(default=False)["button"]:
            break
        angles = []
        for dof in leftArmDofs:
            angle = motors.getPositionDg(dof)
            angles.append(angle)
        goal = points[i]
        error = np.linalg.norm(np.array(angles)-np.array(goal))/len(angles)
        #print(' error',error)
        eps=1.3
        if error < eps:
            i += 1
            if i < len(points):
                #print('point',i)
                setLeftArm(points[i])
            else:
                pass
                #print('done')

#perform([pose0])

def bioforward(pose,w=0.8):
    ps = getLeftArm()
    return [ [w*pose[0]+(1.0-w)*ps[0]]+ps[1:-2]+pose[-2:], pose ]

def biobackward(pose,w=0.0):
    ps = getLeftArm()
    return [ [w*pose[0]+(1.0-w)*ps[0]]+pose[1:], pose ]

class ExperimentAgent(Agent):

    def init(self):
        space.attach_trigger("experiment",self)

    def senseSelectAct(self):
        space["button"] = False
        name = space(default="xxx")["name"]
        file = open("Experiment/" + name + ".txt", "a")
    
        positions = ["A1","A2","A3","A4","A5","A6","A7","A8",
                     "B1","B2","B3","B4","B5","B6","B7","B8",
                     "C1","C2","C3","C4","C5","C6","C7","C8" ]

        samples = random.sample(positions, 5) # 5 == pocet vybranych pozicii
    
        for p in samples:
            file.write(f"Touched: {p}")
            x = ord(p[1])-ord('1')
            y = ord(p[0])-ord('A')
            pose = poses[y][x]

            head = space(default=True)['head']
            if head:
                pose = pose[:-2] + [-2.0, 0.0]
            
            middlePose = []
            for i in range(len(pose)-2):
                middlePose.append((pose[i]+pose0[i])/2)

            middlePose += pose[-2:]

            perform([pose0])
            points = bioforward(middlePose)
            perform(points)

            space["button"] = False

            space["experiment"] = False
            while not space["experiment"]:
                time.sleep(0.5)
            
            predicated = space(default="")["prediction"]
            file.write(f" | Predicated:{predicated} | Head:{head} \n")

            points = bioforward(pose)
            perform(points)
            
            time.sleep(1)
            points = biobackward(pose0) #defaultna poloha
            
            perform(points)

            space["experiment"] = False


        file.close()


#GUI
layout = [
    [ 
        sg.Text("Name", size=(25, 1)), 
        sg.Radio("Head", "moving", True, size=(8, 1), key="Head", enable_events=True),
        sg.Text("Prediction", size=(25, 1)), 
        sg.Button("Run", size=(10, 1)),
        sg.Button("Stop", size=(10, 1)),
        sg.Button("Exit", size=(10, 1)),
    ],
]
window = sg.Window("Experiment", layout, finalize=True)
window['Stop'].bind("<Return>", "_Enter")
head = True
name = ""
while True:
    event, values = window.read(timeout=1)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Head":
        head = values["Head"] == "moving"
        space["head"] = head
    elif event == "Run":
        space["experiment"] = True
    elif event == "Stop":
        space["experiment"] = False
        space["button"] = True
    
    if "name" in values.keys():
        space["name"] = values["name"]
    if "prediction" in values.keys():
        space["prediction"] = values["prediction"]
        
