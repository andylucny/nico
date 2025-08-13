import time
import numpy as np
from keras.models import load_model
from agentspace import Agent, space

from nicomover import move_to_posture, current_posture

model = load_model("pointing.h5") 
arm_dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x']
head_dofs = ['head_z', 'head_y']

class PointAroundAgent(Agent):

    def __init__(self, nameFeatures, nameSupress):
        self.nameFeatures = nameFeatures
        self.nameSupress = nameSupress
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameFeatures,self)

    def senseSelectAct(self):
    
        if space(default=True)[self.nameSupress]:
            return
    
        features = space[self.nameFeatures]
        if features is None:
            return
            
        if len(features) != 384:
            return
        
        head_angles = current_posture(head_dofs).values()
        inputs = list(features) + list(head_angles)
        arm_angles = (model(np.array([inputs]))[0] - 0.5)*360
        posture = dict(zip(arm_dofs,arm_angles))
        move_to_posture(posture)
        time.sleep(1)

# TBD: problem: toto sa moze pustat len ked sa uz robot pozera na objekt priamo
# na to ze je object niekde mimo by v datasete museli byt snimky ked sa robot otaca inam
# a head-z, head-y by museli byt vstupom 