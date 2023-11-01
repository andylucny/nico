from agentspace import Agent, space, Trigger
from nicomotion.Motion import Motion
import numpy as np
import time
import os
from TouchAgent import clean
from speak import speak
import pyautogui
from datetime import datetime

motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

def close():
    global robot
    try:
        print('setting default pose of the robot')
        setLeftArm(pose0[:-2])
        time.sleep(1)
        setDefaultPose()
        print('closing line')
        del robot
        print('line closed')
    except:
        pass

leftArmDofs = ['l_shoulder_z','l_shoulder_y','l_arm_x','l_elbow_y','l_wrist_z','l_wrist_x','l_thumb_z','l_thumb_x','l_indexfinger_x','l_middlefingers_x']
headDofs = ['head_z','head_y']

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

def getHead():
    angles = []
    for dof in headDofs:
        angle = robot.getAngle(dof)
        angles.append(angle)
    return angles

def setLeftArm(angles,duration=2.0):
    for dof,angle in zip(leftArmDofs,angles):
        motor = getattr(robot._robot, dof)
        motor.goto_position(angle,duration=duration,wait=False)

def setHead(angles,duration=2.0):
    for dof,angle in zip(headDofs,angles):
        motor = getattr(robot._robot, dof)
        motor.goto_position(angle,duration=duration,wait=False)

pose0 = [-5.93, 24.13, 22.11, 62.2, 62.29, 40.22, 9.98, 0.04, -180.0, 166.02, 1.1, -1.45] #
# test
# setLeftArm(pose0)
# print(getLeftArm())

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

def setDefaultPose(speed=0.04):
    allDofs = robot.getJointNames()
    poseBase = [1.19, -35.38, -6.81, -20.35, 33.54, 71.52, -6.81, -20.35, 33.54, 71.52, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0] #
    for dof, angle in zip(allDofs,poseBase):
        robot.setAngle(dof,angle,speed)
    time.sleep(3.0)
    
setDefaultPose()
setLeftArm(pose0)

def stopAllMotors():
    for motor in robot._robot.motors:
        motor.goal_position = motor.present_position

def touch(p,duration=2.0):
    x = ord(p[1])-ord('1')
    y = ord(p[0])-ord('A')
    pose = poses[y][x]
    setLeftArm(pose,duration)
    time.sleep(duration+0.2) 
    setLeftArm(pose0,duration)
    time.sleep(duration)

def globalTest(duration=2.0):
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7']:
            print('touching',f+g)
            touch(f+g,duration)
            time.sleep(1)

def calibtouch(p,duration=2.0):
    space['stop'] = False
    print('press enter')
    while not space(default=False)['stop']:
        time.sleep(0.2)
    x = ord(p[1])-ord('1')
    y = ord(p[0])-ord('A')
    pose = poses[y][x]
    setLeftArm(pose,duration)
    space['stop'] = False
    print('press enter')
    while not space(default=False)['stop']:
        time.sleep(0.2)
    setLeftArm(pose0,duration)
    time.sleep(duration)
    print('done')

def globalCalib(duration=2.0):
    for f in ['A','B','C']:
        for g in ['1','2','3','4','5','6','7']:
            print('calib',f+g)
            space('goal',f+g)
            calibtouch(f+g,duration)
            time.sleep(1)

#touch('B1')
#globalTest()

class ExperimentAgent(Agent):

    def ready(self):
        if self.stopped:
            return
        duration = self.duration if self.lastmode == 0 else self.duration*self.lastmode/100.0
        duration *= 0.7 # speed up
        setLeftArm(pose0,duration)
        speak('Preparing. Please, wait.')
        time.sleep(duration)
        if self.stopped:
            return
        clean()
        self.state = 0
        space["experiment"] = False
        if self.stopped:
            return
        if self.mouse is not None:
            pyautogui.moveTo(self.mouse[0], self.mouse[1])
            self.mouse = None
        try:
            for window in pyautogui.getAllWindows():  
                if "Experiment" in window.title:
                    window.activate()
        except:
            pass
        if self.stopped:
            return
        print('Count:',self.count,'Max Count:',space(default=1)["MaxCount"])
        if self.count > 0 and self.count < space(default=1)["MaxCount"]:
            print("running automatically the next experiment")
            space["experiment"] = True
        else:
            self.count = 0
            space["count"] = self.count
            speak('Please enter your name and start the experiment by clicking Run')

    def init(self):
        self.samples = []
        for f in ['A','B','C']:
            for g in ['1','2','3','4','5','6','7']:
                self.samples.append(f+g)
        self.duration = 4.0
        self.lastmode = 0
        self.count = 0
        self.lastName = ""
        self.mouse = None
        self.ready()
        space.attach_trigger("experiment",self,Trigger.NAMES)
        space.attach_trigger("touch",self,Trigger.NAMES)
        space.attach_trigger("stop",self,Trigger.NAMES)
        
    def senseSelectAct(self):
        trigger = self.triggered()
        mode = space(default=40)["StopMode"]
        self.duration = space(default=4)["Duration"]
        if trigger == "experiment":
            if space(default=False)["experiment"]:
                if self.state != 0:
                    self.ready()
                self.mouse = pyautogui.position()
                name = space(default="xxx")["name"]
                if name != self.lastName:
                    self.count = 1
                    self.lastName = name
                else:
                    self.count += 1
                space["count"] = self.count
                if space(default=False)['TellIstructions']:
                    speak("Starting experiment...")
                else:
                    speak('hmm',unconditional=True)
                space["button"] = False
                if mode == 0:
                    time.sleep(1)
                    speak("Please, use button Enter to stop me when you are ready to guess the touch point.")
                self.sample_index = np.random.randint(len(self.samples))
                self.posename = self.samples[self.sample_index]
                x = ord(self.posename[1])-ord('1')
                y = ord(self.posename[0])-ord('A')
                self.touch = touches[y][x]
                space['emulated'] = self.touch
                self.pose = poses[y][x]
                head = space(default=True)['head']
                if not head:
                    self.pose = self.pose[:-2] + pose0[-2:]
                self.timestamp = time.time()
                setLeftArm(self.pose,self.duration)
                self.lastmode = mode
                if mode == 0:
                    self.state = 1
                else:
                    self.timeElapsed = self.duration*mode/100.0
                    time.sleep(self.timeElapsed)
                    stopAllMotors()
                    speak("The movement of my arm has been stopped after "+str(mode)+" percent, please touch the estimated touch point by your finger.")
                    self.state = 2
        elif trigger == "stop":
            if self.state == 1:
                self.timeElapsed = time.time()-self.timestamp
                stopAllMotors()
                speak("You have used the stop button, please touch the estimated touch point by your finger.")
                self.state = 2
            else:
                self.ready()
        elif trigger == "touch":
            record = False
            if self.state == 2:
                self.estimatedTouch = space['touch']
                time.sleep(0.5)
                if mode == 0:
                    speak("Thank you. Let us look on my intention.")
                    self.state = 3
                else:
                    self.intendedTouch = self.touch
                    speak("Thank you.")
                    record = True
                setLeftArm(self.pose,self.duration-self.timeElapsed)
            elif self.state == 3:
                self.intendedTouch = space['touch']
                speak("This was my intention.")
                record = True
            else:
                self.ready()
            if record:
                setLeftArm(pose0,self.duration)
                time.sleep(self.duration+1.0)
                name = space(default="xxx")["name"]
                try:
                    os.mkdir("data/")
                except FileExistsError: 
                    pass
                with open("data/" + name + ".txt", "a") as f:
                    date = str(datetime.now())
                    f.write(f"{date},{self.count},{self.posename},{self.estimatedTouch[0]},{self.estimatedTouch[1]},{self.intendedTouch[0]},{self.intendedTouch[1]},{self.timeElapsed:1.3f}\n")
                speak("Data are recorded.")
                time.sleep(0.5)
                self.ready()
        
if __name__ == "__main__":

    import os
    def quit():
        close()
        os._exit(0)

    from TouchAgent import TouchAgent
    TouchAgent()
    stopAllMotors()
    setLeftArm(pose0)
    
    class SimpleExperimentAgent(Agent):

        def init(self):
            space.attach_trigger('touch',self,Trigger.NAMES)

        def senseSelectAct(self):
            if self.triggered() == 'touch':
                print('save')
                stopAllMotors()
                time.sleep(0.5)
                arm = getLeftArm()
                touch = space['touch']
                goal = space['goal']
                with open('record.txt','at') as f:
                    f.write(str([goal]+list(touch)+list(arm))[1:-1]+'\n')
    
    #SimpleExperimentAgent()
    #print('simple agent started')
    
    #time.sleep(2)
    #touch('B3')
    #globalTest()
    #calibtouch('A1')
    #globalCalib()

"""    
p = 'B3'
x = ord(p[1])-ord('1')
y = ord(p[0])-ord('A')
pose = poses[y][x]
touch = touches[y][x]
clean()
space['emulated'] = touch
duration = 1.0
setHead(pose[-2:],duration)
time.sleep(duration)
duration = 4.0
setLeftArm(pose[:-2],duration)
time.sleep(0.8*duration)
stopAllMotors()
#
duration = 2.0
setLeftArm(pose0[:-2],duration)
setHead(pose0[-2:],duration)
#
"""    

"""
for touchline in touches:
    for touch in touchline:
        space['emulated'] = touch
        time.sleep(0.1)
"""
