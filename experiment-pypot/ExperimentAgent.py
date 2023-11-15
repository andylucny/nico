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

animations_path = './final_position'

def close():
    space["stop"] = True
    global robot
    try:
        print('setting default pose of the robot')
        playAnimationEnd(home1)
        time.sleep(1)
        setDefaultPose()
    except:
        pass
    try:
        print('closing line')
        del robot
        print('line closed')
    except:
        pass

leftArmDofs = ['l_shoulder_z','l_shoulder_y','l_arm_x','l_elbow_y','l_wrist_z','l_wrist_x','l_thumb_z','l_thumb_x','l_indexfinger_x','l_middlefingers_x']
rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y','r_wrist_z','r_wrist_x','r_thumb_z','r_thumb_x','r_indexfinger_x','r_middlefingers_x']
headDofs = ['head_z','head_y']

def enableTorque():
    for dof in leftArmDofs+rightArmDofs+headDofs:
        robot.enableTorque(dof)

def disableTorque():
    for dof in leftArmDofs+rightArmDofs+headDofs:
        robot.disableTorque(dof)

enableTorque()

def getHead():
    angles = []
    for dof in headDofs:
        angle = robot.getAngle(dof)
        angles.append(angle)
    return angles

def changeHead(angles, speed=0.04):
    for dof,angle in zip(headDofs,angles):
        robot.changeAngle(dof,angle,speed)

def setHead(angles,duration=2.0):
    for dof,angle in zip(headDofs,angles):
        motor = getattr(robot._robot, dof)
        motor.goto_position(angle,duration=duration,wait=False)

def loadAnimation(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        concerned_dofs = eval(lines[0])
        recorded_poses = []
        for line in lines[1:]:
            recorded_pose = eval(line[:-1])
            recorded_poses.append(recorded_pose)
        return (concerned_dofs,recorded_poses)
    raise(BaseException(filename+" does not exist"))

def loadAnimations(path):
    global touches, home1, home2, animations
    touches = np.loadtxt(path+'/touches.txt')
    touches = [ tuple(touch.astype(int)) for touch in touches ]
    animations = []
    for i, _ in enumerate(touches):
        recorded_poses = []
        filename = path+'/p'+str(i+1)+'.txt'
        animation = loadAnimation(filename)
        animations.append(animation)
    home1 = loadAnimation(path+'/home1.txt')
    home2 = loadAnimation(path+'/home2.txt')

loadAnimations(path=animations_path)

def playAnimation(animation,deltaTime=0.01,percentage=100,offset=0):
    concerned_dofs, recorded_poses = animation
    defaultSpeed = 0.04*0.5
    for i, pose in enumerate(recorded_poses):
        if i < offset:
            continue
        for dof, angle in zip(concerned_dofs,pose):
            robot.setAngle(dof,angle,defaultSpeed)
        time.sleep(deltaTime)
        if space(default=False)["stop"]:
            return i
        if i*100/len(recorded_poses) >= percentage:
            return i
    return len(recorded_poses)

def playAnimationEnd(animation,speed=0.04):
    concerned_dofs, recorded_poses = animation
    pose = recorded_poses[-1]
    for dof, angle in zip(concerned_dofs,pose):
        robot.setAngle(dof,angle,speed)
        
def setDefaultPose(speed=0.04):
    allDofs = robot.getJointNames()
    poseBase = [1.19, -35.38, -6.81, -20.35, 33.54, 71.52, -6.81, -20.35, 33.54, 71.52, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0, -74.51, 163.3, -15.96, -49.98, -180.0, -180.0] #
    for dof, angle in zip(allDofs,poseBase):
        robot.setAngle(dof,angle,speed)
    time.sleep(3.0)
    
def stopAllMotors():
    for motor in robot._robot.motors:
        motor.goal_position = motor.present_position

setDefaultPose()

def touch(i,back=False): # i = 1 .. 7
    playAnimationEnd(home1)
    time.sleep(3)
    playAnimationEnd(home2)
    time.sleep(1)
    playAnimation(animations[i-1])
    if back:
        time.sleep(1.5)
        playAnimationEnd(home1)
        time.sleep(3)

def globalTest():
    for i in range(7):
        touch(i)

#touch(1)
#globalTest()

class ExperimentAgent(Agent):

    def ready(self):
        if self.stopped:
            return
        duration = self.duration if self.lastmode <= 0 else self.duration*self.lastmode/100.0
        duration *= 0.7 # speed up
        playAnimationEnd(home1, speed = 0.06)
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
                name = space(default="+++")["name"]
                if name != self.lastName:
                    self.count = 1
                    self.lastName = name
                else:
                    self.count += 1
                space["count"] = self.count
                if space(default=False)['TellIstructions']:
                    speak("Starting experiment...")
                playAnimationEnd(home2)
                time.sleep(1)
                if mode == 0:
                    time.sleep(1)
                    speak("Please, use button Enter to stop me when you are ready to guess the touch point.")
                self.sample_index = np.random.randint(len(touches))
                self.posename = str(self.sample_index+1)
                print("SELECTED POINT No.",self.posename)
                self.touch = touches[self.sample_index]
                space['emulated'] = self.touch
                self.headMode = space(default=True)['head']
                if self.headMode:
                    self.head = [0,-30]
                else:
                    self.head = [0,0]
                setHead(self.head)
                time.sleep(1)
                self.animation = animations[self.sample_index]
                self.timestamp = time.time()
                space["stop"] = False
                self.lastmode = mode
                self.offset = playAnimation(self.animation,deltaTime=0.01,percentage=mode if mode>0 else 100)
                self.timeElapsed = time.time()-self.timestamp
                if mode == 0:
                    perc = int(100*self.offset/len(self.animation[1]))
                    speak("You have used the stop button at "+str(perc)+" percent, please touch the estimated touch point by your finger.")
                else:
                    speak("The movement of my arm has been stopped after "+str(mode)+" percent, please touch the estimated touch point by your finger.")
                self.timestamp2 = time.time()
                self.state = 2
                space['touch'] = None
        elif trigger == "touch" and space['touch'] is not None:
            if self.state == 2:
                self.timeElapsed2 = time.time()-self.timestamp2
                self.estimatedTouch = space['touch']
                time.sleep(0.5)
                if space(default=False)['CompleteTouch']:
                    speak("Thank you. Let us look on my intention.")
                    playAnimation(self.animation,deltaTime=0.01,offset=self.offset)
                    speak("This was my intention.")
                else:
                    speak("Thank you.")
                    record = True
                name = space(default="+++")["name"]
                try:
                    os.mkdir("data/")
                except FileExistsError: 
                    pass
                with open("data/" + name + ".txt", "a") as f:
                    date = str(datetime.now())
                    f.write(f"{date},{self.count},{self.lastmode},{self.headMode},{self.posename},{self.estimatedTouch[0]},{self.estimatedTouch[1]},{self.touch[0]},{self.touch[1]},{self.timeElapsed:1.3f},{self.timeElapsed2:1.3f}\n")
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
       
    time.sleep(2)
    space['ShowIntention'] = True
    for point in touches:
        space['emulated'] = point
        time.sleep(0.1)
    
    touch(1)
    #globalTest()

