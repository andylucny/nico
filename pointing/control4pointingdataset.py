import time
import os
import signal
import re
import base64
import numpy as np
import cv2 as cv

from agentspace import Agent, space, Trigger

from nicomover import setAngle, getAngle, enableTorque, disableTorque, park, release
from nicomover import current_posture, move_to_posture, load_movement, play_movement, save_movement

from dino import dino_visualization

class ControlAgentForPointingDataset(Agent):
    
    def init(self):
        self.arm_dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x'] + ['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x']
        self.hand_dofs = ['r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x']
        self.head_dofs = ['head_z','head_y']
        enableTorque(self.hand_dofs)
        move_to_posture(dict(zip(self.hand_dofs,[-1.0, 44.0, -179.0, 38.0])))
        space['tospeak'] = "whistle for a shorter time to start"
        time.sleep(3)
        disableTorque(self.arm_dofs)
        space.attach_trigger('clipFeatures',self,Trigger.NAMES)
        space.attach_trigger('whistle',self,Trigger.NAMES)        
        self.postures = []
        self.state = 0
        enableTorque(self.arm_dofs)
        self.dontLook()

    def speak(self, text):
        space(validity=0.1)['tospeak'] = text

    def dontLook(self):
        space['dontLook'] = True

    def lookAround(self):
        space['dontLook'] = False

    def match(self,pattern,text):
        search = re.search(pattern,text)
        if search is None:
            self.groups = []
            return False
        else:
            self.groups = search.groups()
            return True
    
    def matched(self):
        return self.groups

    def senseSelectAct(self):
        changed = self.triggered()
        if changed == 'clipFeatures':
        
            frame = space['robotEye']
            if frame is not None:
                self.frame = frame
                self.clipFeatures = np.copy(space['clipFeatures'])
                self.dinoFeatures = np.copy(space['dinoFeatures'])
                self.points = space(default=[None]*6)["dinoPoints"]
                result = dino_visualization(frame,np.zeros(frame.shape[:2],np.uint8),self.points)
                fps = space["fps"]
                if fps is not None:
                    cv.putText(result, f"{fps:1.0f}", (8,25), 0, 1.0, (0, 255, 0), 2)

                cv.imshow('NICO pointing',result)
                key = cv.waitKey(1) & 0xff
                if key == 27:
                    self.stopped = True
                    quit()           
            
        elif changed == 'whistle':
            whistle = space(default=0)['whistle']

            if whistle == 1:
            
                if self.state == 0:
                    disableTorque(self.arm_dofs)
                    space['tospeak'] = "torque disabled, set a posture and whistle"
                elif self.state == 1:
                    enableTorque(self.arm_dofs)
                    self.lookAround()
                    space['tospeak'] = "torque enabled, head moving, expose the object and whistle"
                elif self.state == 2:
                    self.dontLook()
                    space['tospeak'] = "head stopped, whistle for a longer time to save a sample"

                self.state = self.state + 1 if self.state < 3 else 0

                time.sleep(2)
                
            elif whistle == 2:

                dofs = self.arm_dofs+self.hand_dofs+self.head_dofs
                lens = []
                posture = current_posture(dofs)
                posture = list(posture.values())
                lens.append(len(posture))
                
                dofs += [ f'point{coord}{i}' for i in range(len(self.points)) for coord in ['x','y'] ]
                flattened_points = [coordinate for point in self.points for coordinate in point]
                posture += flattened_points
                lens.append(len(flattened_points))
                
                dofs += [ f'dino{i}' for i in range(len(self.dinoFeatures)) ]
                posture += list(self.dinoFeatures)
                lens.append(len(list(self.dinoFeatures)))

                dofs += [ f'clip{i}' for i in range(len(self.clipFeatures[0])) ]
                posture += list(self.clipFeatures[0])
                lens.append(len(list(self.clipFeatures[0])))
                
                _, buffer = cv.imencode('.jpg', self.frame)
                dofs += [ 'frame' ]
                posture += [base64.b64encode(buffer).decode('utf-8')]
                lens.append(1)
                
                print('saved ',lens,'=',np.sum(lens))
                
                self.postures.append(dict(zip(dofs,posture)))
                save_movement('pointing_dataset.txt',self.postures)
                
                space['tospeak'] = "saved, whistle shortly for disabling torque or for a longer time to save a next sample"
                time.sleep(3)
                               
            space['whistle'] = 0
