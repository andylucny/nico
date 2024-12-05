import numpy as np
import cv2 as cv
from agentspace import Agent, space
from WhistleAgent import WhistleAgent
from ActionAgent import ActionAgent
import time
import os
import signal

def quit():
    #Agent.stopAll()
    os._exit(0)

# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

WhistleAgent()
time.sleep(1)
ActionAgent()
time.sleep(1)

from ActionAgent import getRange, get, set, setone, save

carlo_matilde_position_dofs = ['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x', 'l_thumb_z', 'l_thumb_x', 'l_indexfinger_x', 'l_middlefingers_x', 'r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x']
#carlo_matilde_position_values = [-23.0, 14.0, 0.0, 103.0, -1.0, -55.0, -62.0, -180.0, -179.0, -176.0, -25.0, 83.0, 47.0, 94.0, -59.0, 114.0, 170, 115, 172, 28.0] # 0.0, 44.0, -179.0, 138.0
carlo_matilde_position_values = [-23.0, 14.0, 0.0, 103.0, -1.0, -55.0, -62.0, -180.0, -179.0, -176.0, -25.0, 83.0, 47.0, 94.0, -59.0, 114.0, -130, 4, 172, 180] # 0.0, 44.0, -179.0, 138.0
for dof, value in zip(carlo_matilde_position_dofs,carlo_matilde_position_values):
    setone(dof,value)

carlo_matilde_position = [-25.0, 83.0, 47.0, 94.0, -59.0, 28] #114.0
#touch_position = [30.0, 40.0, 20.0, 131.0, 161.0, 146.0] # touch 1
touch_position = [32.0, 31.0, 14.0, 116.0, 167.0, 156.0, 3, -30] # touch 2
#touch_position = [47.0, 46.0, 26.0, 141.0, 157.0, 142.0, 7, -29] # touch 3
#touch_position = [50.0, 54.0, 35.0, 157.0, 148.0, 134.0, 3, -29] # touch 4
#touch_position = [35.0, 51.0, 31.0, 151.0, 151.0, 137.0, -3, -29] # touch 5
#touch_position = [18.0, 41.0, 19.0, 132.0, 161.0, 147.0, -7, -29] # touch 6
#touch_position = [17.0, 29.0, 12.0, 112.0, 168.0, 159.0, -3, -30] # touch 7

rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y','r_wrist_z','r_wrist_x','r_indexfinger_x']

import PySimpleGUI as sg
sg.theme("LightGreen")
slider_v = 36
slider_h = 10
layout = []    
for i, dof in enumerate(rightArmDofs):
    key = dof
    minVal, maxVal, defVal = getRange(key) 
    layout.append([ 
        sg.Text(key, size=(19, 1)), 
        sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key=key, enable_events=True)
    ])

def update(pose):
    for dof, value in zip(rightArmDofs, pose):
        window[dof].update(value=value)

layout.append([
    sg.Button("Carlo-Matilde", size=(20, 1)),
    sg.Button("Touch", size=(12, 1)),
    sg.Button("Save", size=(8, 1)),
])
layout.append([
    sg.Button("Shoot", size=(8, 1)),
    sg.Button("Replay", size=(8, 1)),
    sg.Button("Exit", size=(8, 1)),
])

window = sg.Window("Nico control GUI", layout, finalize=True)
window.bind("<Key-->", "Current-")
window.bind("<Key-+>", "Current+")
for dof in rightArmDofs: 
    window[dof].bind('<ButtonRelease-1>', ' Release')
    window[dof].bind('<ButtonPress-1>', ' Press')

lastdof = None
t0 = int(time.time())
while True:
    event, values = window.read(timeout=100)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "__TIMEOUT__":
        t1 = int(time.time())
        if t1 > t0:
           pose = get()
           update(pose)
           t0 = t1
    elif event == "Current-":
        if lastdof is not None:
            lastvalue -= 1
            setone(lastdof, lastvalue)
            #print(lastdof, '<=', lastvalue)
    elif event == "Current+":
        if lastdof is not None:
            lastvalue += 1
            setone(lastdof, lastvalue)
            #print(lastdof, '->', lastvalue)
    elif 'Press' in event:
        for dof in rightArmDofs: 
            if dof in event:
                lastdof = dof
                lastvalue = values[lastdof]
    elif 'Release' in event:
        pass
    elif event in rightArmDofs:
        lastdof = event
        lastvalue = values[lastdof]
        setone(lastdof, lastvalue)
        #print(lastdof, ':=', lastvalue)
    elif event == "Carlo-Matilde":
        set(carlo_matilde_position)
    elif event == "Touch":
        set(touch_position)
    elif event == "Save":
        save(get())
    elif event == "Shoot":
        posture = get()
    elif event == "Replay":
        #set(get()) # kontinualne klesa
        #set(pose) # kontinualne klesa
        set(posture)
    else:
        print('event',event)

quit()
