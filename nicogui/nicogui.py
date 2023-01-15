import time
import PySimpleGUI as sg
import cv2
import numpy as np
from nicomotors import NicoMotors

motors = NicoMotors('COM6')
dofs = motors.dofs()
try:
    motors.open()
except:
    print('motors are not operational')

sg.theme("LightGreen")

slider_v = 32 #18
slider_h = 10
degrees = True

def side_layout(kind='Left', id=0): #id=10
    layout = [
        [ sg.Text(kind, size=(10, 1), justification="left"), sg.Image(filename="", key=kind+"-EYE") ],
    ]
    texts = ["Arm","","","Elbow","Wrist","","Thumb","","Forefinger","Little fingers"]
    for i in range(10):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        layout.append([ 
            sg.Text(texts[i], size=(10, 1)), 
            sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key=key),
        ])
    return layout
    
def update_side_layout(kind='Left', id=0): #id=10
    for i in range(10):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        window[key].update(range=(minVal, maxVal),value=defVal)

def addons_layout(id=20):
    layout = [
        [ sg.Text("Units", size=(10, 1)), sg.Radio("Bins", "Units", False, size=(10, 1)), sg.Radio("Degrees", "Units", True, size=(10, 1)) ],
        [ sg.Text("Torque", size=(10, 1)), sg.Radio("Off", "Torque", False, size=(10, 1)), sg.Radio("On", "Torque", True, size=(10, 1)) ],
        [ sg.Text("Synchronize", size=(10, 1)), sg.Radio("Off", "Synchro", True, size=(10, 1)), sg.Radio("On", "Synchro", False, size=(10, 1)) ]
    ]
    layout.append([ sg.HSeparator() ])
    texts = ["Neck up-down","Neck left-right"]
    for i in range(2):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        layout.append([ sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key=key) ])
        layout.append([ sg.Text(texts[i], size=(10, 1))])
    layout.append([ sg.HSeparator() ])
    layout.append([ sg.Push(), sg.Button("Set default position", size=(20, 1)) ])    
    layout.append([ sg.VPush() ])
    layout.append([ sg.Push(), sg.Button("Exit", size=(10, 1)) ])
    return layout
    
def update_addons_layout(id=20):
    for i in range(2):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        window[key].update(range=(minVal, maxVal),value=defVal)
    
layout = [[
    sg.Column(side_layout('Left',0), vertical_alignment='top'), 
    sg.VSeparator(),
    sg.Column(side_layout('Right',10), vertical_alignment='top'),      
    sg.VSeparator(),
    sg.Column(addons_layout(20), vertical_alignment='top', expand_y=True)   
]]

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
fps = 30 
cap.set(cv2.CAP_PROP_FPS,fps)    

# Create the window and show it without the plot
window = sg.Window("Nico control GUI", layout, finalize=True)

window.bind("<Escape>", "Exit")
for k in dofs:
    window[k].bind('<ButtonRelease-1>', 'Click')
window.bind("<Key-->", "Current-")
window.bind("<Key-+>", "Current+")

for k in dofs:
    motors.enableTorque(k)
torque = True

synchro = False
def synchronized(key):
    if 'left-' in key:
        return key.replace('left-','right-')
    elif 'right-' in key:
        return key.replace('right-','left-')
    else:
        return key

current = dofs[0]
last_values = None
t0 = int(time.time()//2)
while True:
    event, values = window.read(timeout=20)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Set default position":
        if not torque:
            torque = True
            window['Torque'].update(value="On")
            for k in dofs:
                motors.enableTorque(k)
        for k in dofs:
            motors.setDefaultPosition(k)

    if last_values is None:
        last_values = values
    elif last_values != values:
        for k in values.keys():
            if last_values[k] != values[k]:
                #print(k,'->',values[k])
                if isinstance(k,int) and k == 3:
                    if values[k]:
                        degrees = True
                        print('degrees on')
                    else:
                        degrees = False
                        print('degrees off')
                    update_side_layout('Left',0)
                    update_side_layout('Right',10)
                    update_addons_layout(20)
                elif isinstance(k,int) and k == 5:
                    if values[k]:
                        torque = True
                        print('torque on')
                        for kk in dofs:
                            motors.enableTorque(kk)
                    else:
                        torque = False
                        print('torque off')
                        for kk in dofs:
                            motors.disableTorque(kk)
                elif isinstance(k,int) and k == 7:
                    synchro = values[k]
                    print('synchonization on' if synchro else 'synchronization off')
                elif isinstance(k, str) and k in dofs: #'Click' in event and 
                    if torque:
                        print('set',k,'to',values[k])
                        if synchro:
                            ks = synchronized(k)
                            if ks != k:
                                print('set',ks,'to',values[k])
                        if degrees:
                            motors.setPositionDg(k,int(values[k]))
                            if synchro and ks != k:
                                motors.setPositionDg(ks,int(values[k]))
                        else:
                            motors.setPosition(k,int(values[k]))
                            if synchro and ks != k:
                                motors.setPosition(ks,int(values[k]))
        last_values = values

    if 'Click' in event:
        current = event[:-len('Click')]
    elif 'Current' in event:
        if torque:
            diff = -1.0 if event[-1] == '-' else 1.0
            if not degrees:
                diff *= 5
            minVal, maxVal, _ = motors.getRangeDg(current) if degrees else motors.getRange(current)
            oldValue = values[current]
            newValue = max(min(oldValue+diff,maxVal),minVal)
            #print(oldValue,'->',newValue)
            if oldValue != newValue:
                window[current].update(value=newValue)
                last_values[current] = newValue
                print('set',current,'to',newValue)
                if synchro:
                    currents = synchronized(current)
                    if currents != current:
                        print('set',currents,'to',newValue)  
                if degrees:
                    motors.setPositionDg(current,int(newValue))
                    if synchro and currents != current:
                        motors.setPositionDg(currents,int(newValue))
                else:
                    motors.setPosition(current,int(newValue))
                    if synchro and currents != current:
                        motors.setPosition(currents,int(newValue))
    else:
        t1 = int(time.time()//2)
        if t0 != t1:
            for k in dofs:
                position = motors.getPositionDg(k) if degrees else motors.getPosition(k)
                window[k].update(value = position)
                last_values[k] = float(position)
            
    _, frame = cap.read()
    if frame is not None:
        imgbytes = cv2.imencode(".png", cv2.resize(frame,(320,240)))[1].tobytes()
        window["Left-EYE"].update(data=imgbytes)
        window["Right-EYE"].update(data=imgbytes)

window.close()

