from agentspace import Agent, space
from mover3 import enableTorque, play_movement
import numpy as np
from keras.models import load_model
import time
from pprint import pprint
        
rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y','r_wrist_z','r_wrist_x','r_thumb_z','r_thumb_x','r_indexfinger_x','r_middlefingers_x']
parking_position = [-8.0, -15.0, 16.0, 74.0, -24.0, 35.0, -71.0, -104.0, -180.0, -180.0, 0]
ready_position = [-8.0, 46.0, 13.0, 99.0, 44.0, 99.0, -70.0, 32.0, -180.0, 180.0, 510]
steady_position = [13.0, 36.0, 25.0, 106.0, 66.0, -180.0, -70.0, 26.0, -180.0, 172.0, 800]
resolution = (2400, 1350)
model = load_model("right.h5") # "perceptron.h5"

class MotionAgent(Agent):
            
    def init(self):
        enableTorque(rightArmDofs)
        self.ind = 0
        space.attach_trigger("touch",self)

    def senseSelectAct(self):
        point = space["touch"]
        if point is None:
            return
        if point[0] < 0 or point[1] < 0:
            return
        
        inps = np.array([point],np.float32) / np.array([resolution],np.float32)
        print('inps'); pprint(inps[0])
        outs = model(inps).numpy()[0]
        print('outs'); pprint(outs)
        
        if outs[3] > 1.0: # elbow
            print('not possible')
            space(validity=0.5)["text"] = "I cannot reach that spot."
            time.sleep(1.5)
            return
            
        if outs[5] > 1.0: # wrist-x
            outs[5] = 1.0
        
        space(validity=0.5)["text"] = "O.K."
        
        touch_angles = list(np.round(outs*180))
        print('angles'); pprint(touch_angles)
        touch_timestamp = 1250 + outs[0]*250
        print('timestamp',touch_timestamp)
        poses = [
            parking_position[:-1],
            ready_position[:-1],
            steady_position[:-1],
            [ (angle if index != 5 else -180.0) for index, angle in enumerate(touch_angles) ],
            touch_angles,
            touch_angles,
            ready_position[:-1],
            steady_position[:-1],
            parking_position[:-1]
        ]
        print('poses'); pprint(poses)
        durations = [
            1.500,
            (ready_position[-1]-parking_position[-1])/1000.0,
            (steady_position[-1]-ready_position[-1])/1000.0,
            round(touch_timestamp-steady_position[-1])/1000.0,
            0.25,
            0.5,
            round(touch_timestamp-steady_position[-1])/1000.0,
            (steady_position[-1]-ready_position[-1])/1000.0,
            (ready_position[-1]-parking_position[-1])/1000.0
        ]
        print('durations'); pprint(durations)
        
        play_movement(rightArmDofs,poses,durations)
        self.ind += 1
        np.savetxt(f'touch-{self.ind}',touch_angles)
        print('moved')
        
        space["touch"] = (-1,-1)
        time.sleep(1.0)
