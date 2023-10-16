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

GuiAgent()
time.sleep(1)
TouchAgent()
time.sleep(1)
ExperimentAgent()
time.sleep(1)
CameraAgent('HD Pro Webcam C920',1,'humanImage',10)
time.sleep(1)
CameraAgent('HD Pro Webcam C920',0,'robotImage',10)
time.sleep(1)
RecorderAgent()
