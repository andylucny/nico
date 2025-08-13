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

def quit():
    release()
    os._exit(0)

def signal_handler(signal, frame): 
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

from CameraAgent import CameraAgent
from PerceptionAgent import PerceptionAgent
from LookAroundAgent import LookAroundAgent
from PointAroundAgent import PointAroundAgent
from SpeakerAgent import SpeakerAgent

CameraAgent('See3CAM_CU135',1,'robotEye',fps=10,zoom=350) # right eye
time.sleep(1)
PerceptionAgent('robotEye','clipFeatures','dinoPoints') # -> 'dinoFeatures'
time.sleep(1)
LookAroundAgent('dinoPoints','dontLook')
time.sleep(1)
PointAroundAgent('dinoFeatures','dontPoint')
time.sleep(1)
SpeakerAgent('tospeak')
time.sleep(1)

#space['dontPoint'] = False

# the pointing dataset collection
from WhistleAgent import WhistleAgent
WhistleAgent() # 1, 2 -> 'whistle'
time.sleep(1)
from control4pointingdataset import ControlAgentForPointingDataset
ControlAgentForPointingDataset()


