import time
import os
import PySimpleGUI as sg
import cv2
import numpy as np
from nicomotors import NicoMotors
from nicocameras import NicoCameras
def quit():
    os._exit(0)

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
    layout = [[
        sg.Column([
            [ sg.Text(kind, size=(5, 1), justification="left") ],
            [ sg.Text("", size=(5, 1), justification="left", key=kind+"-FPS") ]
        ], vertical_alignment='middle'), 
        sg.Image(filename="", key=kind+"-EYE") 
    ]]
    texts = ["Arm","","","Elbow","Wrist","","Thumb","","Forefinger","Little fingers"]
    for i in range(10):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        layout.append([ 
            sg.Text(texts[i], size=(10, 1)), 
            sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key=key),
        ])
    return layout
    
def addons_layout(id=20):
    layout = [
        [ sg.Text("Units", size=(10, 1)), sg.Radio("Bins", "Units", False, size=(8, 1), key="Units-Bin"), sg.Radio("Degrees", "Units", True, size=(8, 1), key="Units-Degrees") ],
        [ sg.Text("Torque", size=(10, 1)), sg.Radio("Off", "Torque", False, size=(8, 1), key="Torque-Off"), sg.Radio("On", "Torque", True, size=(8, 1), key="Torque-On") ],
        [ sg.Text("Synchronize", size=(10, 1)), sg.Radio("Off", "Synchro", True, size=(8, 1), key="Synchro-Off"), sg.Radio("On", "Synchro", False, size=(8, 1),key="Synchro-On") ]
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
    layout.append([ sg.HSeparator() ])
    layout.append([ 
        sg.Text("Capture", size=(6, 1)), 
        sg.Text("0", size=(4,1), key="Captured"),
        sg.Push(), 
        sg.Radio("Pose", "Mode of Recording", True, size=(5, 1), key="Mode-Pose"),
        sg.Radio("Movement", "Mode of Recording", False, size=(10, 1), key="Mode-Movement")
    ])
    layout.append([  
        sg.Text("Period", size=(6, 1)),
        sg.Slider((1,5000), 500, 1, orientation="h", size=(20, 10), key="Period"),
        sg.Text("ms", size=(2, 1))
    ])
    layout.append([
        sg.Button("Start", size=(5, 1), key="Start Recording"),
        sg.Button("Stop", size=(5, 1), key="Stop Recording"),
        sg.Input(key="Save Recording", enable_events=True, visible=False),
        sg.FileSaveAs(button_text='Save', size=(5, 1), initial_folder=os.getcwd(), tooltip="save recorded data into a file", file_types=(("text files", "*.txt"),), target="Save Recording"),
        sg.Input(key="Load Recording", enable_events=True, visible=False),
        sg.FileBrowse(button_text='Load', size=(5, 1), initial_folder=os.getcwd(), tooltip="load recorded data from a file", file_types=(("text files", "*.txt"),), target="Load Recording"),
        sg.Button("Replay", size=(5, 1), key="Replay Recording")
    ])    
    layout.append([ sg.VPush() ])
    layout.append([ sg.Push(), sg.Button("Exit", size=(10, 1)) ])
    return layout
       
layout = [[
    sg.Column(side_layout('Left',0), vertical_alignment='top'), 
    sg.VSeparator(),
    sg.Column(side_layout('Right',10), vertical_alignment='top'),      
    sg.VSeparator(),
    sg.Column(addons_layout(20), vertical_alignment='top', expand_y=True)   
]]

cameras = NicoCameras()

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

period = 500
mode = True #pose
window["Stop Recording"].update(text='Next')
record = False
recorded = []
window["Captured"].update(value=str(len(recorded)))
replaying = False
replay = -1
current = dofs[0]
last_values = None
t0 = int(time.time()*1000/period)
while True:
    event, values = window.read(timeout=20)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Set default position":
        if not torque:
            torque = True
            window["Torque-On"].update(value=True)
            for k in dofs:
                motors.enableTorque(k)
        for k in dofs:
            motors.setDefaultPosition(k)

    if last_values is None:
        last_values = values
    elif last_values != values:
        for k in values.keys():
            if last_values[k] != values[k] and isinstance(k,str):
                #print(k,'->',values[k])
                if k == "Units-Degrees":
                    if values[k]:
                        degrees = True
                        print('degrees on')
                    else:
                        degrees = False
                        print('degrees off')
                    for kk in dofs:
                        if degrees:
                            values[kk] = float(motors.bin2dg(kk,values[kk]))
                            minVal, maxVal, _ = motors.getRangeDg(kk)
                        else:
                            values[kk] = float(motors.dg2bin(kk,values[kk]))
                            minVal, maxVal, _ = motors.getRange(kk)
                        window[kk].update(range=(minVal, maxVal), value = values[kk])
                        last_values[kk] = values[kk]
                    break
                elif k == "Torque-On":
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
                    break
                elif k == "Synchro-On":
                    synchro = values[k]
                    print('synchonization on' if synchro else 'synchronization off')
                    break
                elif k == "Mode-Pose":
                    if values[k]:
                        mode = True
                        print('record pose')
                    else:
                        mode = False
                        print('record movement')
                    record = False
                    replay = -1
                    window["Stop Recording"].update(text="Stop" if mode else "Next")
                    break
                elif k in dofs: #'Click' in event and 
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
                elif k == "Period":
                    period = int(values["Period"])
                    if period < 10:
                        pass
                    elif period < 100:
                        period = 10*(period//10)
                    elif period < 1000:
                        period = 100*(period//100)
                    else:
                        period = 500*(period//500)
                    window["Period"].update(value=float(period))
                    print("Period:",period)
                elif k == "Save Recording" and values[k] != "":
                    filename = values[k]
                    with open(filename, 'w') as f:
                        for r in recorded:
                            f.write(str(r)+'\n')
                    window["Save Recording"].update(value='')
                    values[k] = ''
                    print('saved')
                elif k == "Load Recording" and values[k] != "":
                    filename = values[k]
                    recorded = []
                    with open(filename, 'r') as f:
                        for line in f.readlines():
                            r = eval(line[:-1])
                            recorded.append(r)
                    window["Captured"].update(value=str(len(recorded)))
                    window["Load Recording"].update(value='')
                    values[k] = ''
                    print('loaded')
                
        last_values = values

    if 'Click' in event:
        current = event[:-len('Click')]
    elif last_values is None:
        pass
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
    elif 'Start Recording' in event:
        print('recording started')
        recorded = []
        window["Captured"].update(value=str(len(recorded)))
        record = True
        window["Stop Recording"].update(text='Next')
    elif 'Stop Recording' in event:
        if mode:
            print('record next')
            record = True
        else:
            print('recording stopped')
            record = False
    elif 'Replay Recording' in event:
        replaying = True
        print('replaying','one' if mode else 'many','...')
    
    t1 = int(time.time()*1000/period)
    if t0 != t1:
        t0 = t1
        for k in dofs:
            position = motors.getPositionDg(k) if degrees else motors.getPosition(k)
            window[k].update(value = position)
            last_values[k] = float(position)
        if record:
            recorded.append([last_values[k] for k in dofs] if degrees else [motors.bin2dg(k,last_values[k]) for k in dofs])
            window["Captured"].update(value=str(len(recorded)))
            if mode:
                record = False
                print("recorded")
        elif replaying:
            replay += 1
            if replay >= len(recorded):
                replay = -1
                replaying = False
                print('...replayed many')
            else:
                for positionDg, k in zip(recorded[replay],dofs):
                    position = positionDg if degrees else motors.dg2bin(k,positionDg)
                    motors.setPositionDg(k,position)
                    window[k].update(value = position)
                    last_values[k] = float(position)
                if mode:
                    replaying = False
                    print('...replayed one')
        
    left_frame, right_frame = cameras.read()
    left_fps, right_fps = cameras.fps()
    if left_frame is not None and left_fps > 1: 
        left_imgbytes = cv2.imencode(".png", cv2.resize(left_frame,(320,240)))[1].tobytes()
        window["Left-EYE"].update(data=left_imgbytes)
        window["Left-FPS"].update(value=str(left_fps))
        if right_frame is None or right_fps <= 1:
            window["Right-EYE"].update(data=left_imgbytes)
            window["Right-FPS"].update(value="")
    if right_frame is not None and right_fps > 1:
        right_imgbytes = cv2.imencode(".png", cv2.resize(right_frame,(320,240)))[1].tobytes()
        window["Right-EYE"].update(data=right_imgbytes)
        window["Right-FPS"].update(value=str(right_fps))

window.close()
motors.close()
cameras.close()
#os._exit(0)

