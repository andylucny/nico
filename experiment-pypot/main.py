import time
import os
import signal
from ExperimentAgent import close

def quit():
    close()
    os._exit(0)

# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

from download import download_all
download_all()

from ExperimentAgent import ExperimentAgent
from GuiAgent import GuiAgent
from TouchAgent import TouchAgent
from CameraAgent import CameraAgent
from RecorderAgent import RecorderAgent

GuiAgent() # writes 'experiment', 'stop' reads 'humanImage', 'robotImage', 'robotEye', 'robotWideFOV'
time.sleep(1)
TouchAgent() # writes 'touch', 'stop', 'experiment', 'touchImage' reads 'emulated'
time.sleep(1)
ExperimentAgent()
time.sleep(1)
CameraAgent('HD Pro Webcam C920',1,'humanImage',fps=10)
time.sleep(1)
CameraAgent('HD Pro Webcam C920',0,'robotImage',fps=10)
time.sleep(1)
CameraAgent('See3CAM_CU135',0,'robotEye',fps=10,zoom=350)
time.sleep(1)
CameraAgent('See3CAM_CU135',1,'robotWideFOV',fps=10,zoom=100)
time.sleep(1)
RecorderAgent() # reads 'humanImage', 'robotImage', 'robotEye', 'touchImage'
