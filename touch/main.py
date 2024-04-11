import time
import os
import signal
from agentspace import Agent, space
from mover3 import close

def quit():
    Agent.stopAll()
    close()
    os._exit(0)

# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

#from download import download_all
#download_all()

from MotionAgent import MotionAgent
from TouchAgent import TouchAgent

MotionAgent() 
time.sleep(1)
TouchAgent() 
time.sleep(1)
