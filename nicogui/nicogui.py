import time
import os
import signal
import PySimpleGUI as sg
import cv2
import numpy as np
from beeply.notes import beeps
from nicomotors import NicoMotors
from nicocameras import NicoCameras

def quit():
    os._exit(0)

# exit on ctrl-c
def signal_handler(signal, frame):
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

motors = NicoMotors()
dofs = motors.dofs()
try:
    motors.open()
except:
    print('motors are not operational')

groups = {}
groups['left-arm'] = [k for k in dofs[:6]]
groups['left-hand'] = [k for k in dofs[6:10]]
groups['right-arm'] = [k for k in dofs[10:16]]
groups['right-hand'] = [k for k in dofs[16:20]]
groups['head'] = [k for k in dofs[20:]]

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
            sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key=key)
        ])
    return layout
    
def addons_layout(id=20):
    layout = [
        [ 
            sg.Text("Units", size=(10, 1)), 
            sg.Radio("Bins", "Units", False, size=(8, 1), key="Units-Bin", enable_events=True), 
            sg.Radio("Degrees", "Units", True, size=(8, 1), key="Units-Degrees", enable_events=True) 
        ],
        [ 
            sg.Text("Torque", size=(10, 1)), 
            sg.Radio("Off", "Torque", False, size=(8, 1), key="Torque-Off", enable_events=True), 
            sg.Radio("On", "Torque", True, size=(8, 1), key="Torque-On", enable_events=True) 
        ],
        [ 
            sg.Text("Synchronize", size=(10, 1)), 
            sg.Radio("Off", "Synchro", True, size=(5, 1), key="Synchro-Off", enable_events=True), 
            sg.Radio("On", "Synchro", False, size=(4, 1),key="Synchro-On", enable_events=True),
            sg.Radio("Reverse", "Synchro", False, size=(7, 1),key="Synchro-Reverse", enable_events=True) 
        ]
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
        sg.Radio("Pose", "Mode of Recording", True, size=(5, 1), key="Mode-Pose", enable_events=True),
        sg.Radio("Movement", "Mode of Recording", False, size=(10, 1), key="Mode-Movement", enable_events=True)
    ])
    layout.append([  
        sg.Text("Period", size=(6, 1)),
        sg.Slider((1,5000), 1000, 1, orientation="h", size=(20, 10), key="Period", enable_events=True),
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
    layout.append([ 
        sg.Checkbox('left arm  ', default=True, key='concern-left-arm', enable_events=True), 
        sg.Checkbox('left hand ', default=True, key='concern-left-hand', enable_events=True), 
        sg.Push(), 
        sg.Text("0", size=(4,1), key="Replayed", visible=False) 
    ])
    layout.append([ 
        sg.Checkbox('rigth arm', default=True, key='concern-right-arm', enable_events=True), 
        sg.Checkbox('right hand', default=True, key='concern-right-hand', enable_events=True), 
        sg.Checkbox('head', default=True, key='concern-head', enable_events=True),
    ])
    layout.append([ 
        sg.Checkbox('beep', default=True, key='beep', enable_events=True)
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

beeper = beeps(250)

# Create the window and show it without the plot
window = sg.Window("Nico control GUI", layout, finalize=True)

window.bind("<Escape>", "Exit")
for k in dofs:
    window[k].bind('<ButtonRelease-1>', ' Release')
    window[k].bind('<ButtonPress-1>', ' Press')
window.bind("<Key-->", "Current-")
window.bind("<Key-+>", "Current+")

for k in dofs:
    motors.enableTorque(k)
torque = True

synchro = 0
def synchronized(key):
    if 'left-' in key:
        return key.replace('left-','right-')
    elif 'right-' in key:
        return key.replace('right-','left-')
    else:
        return key

def synchronizable(key,basekey):
    return ('left-' in basekey and 'right-' in key) or ('right-' in basekey and 'left-' in key)

beep = True
period = 1000
mode = True #pose
window["Stop Recording"].update(text='Next')
record = False
recorded = []
concerned_dofs = []
window["Captured"].update(value=str(len(recorded)))
replaying = False
replay = -1
current = dofs[0]
pressed = { k:False for k in dofs }
concerned = { k:True for k in dofs }
t0 = int(time.time()*1000/period)
while True:
    event, values = window.read(timeout=1)
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

#    if event != '__TIMEOUT__':
#    print(event)
        
    if 'Press' in event:
        for k in dofs:
            if k in event:
                print(k,' pressed')
                pressed[k] = True
    elif 'Release' in event:
        for k in dofs:
            if k in event:
                print(k,' released',values[k])
                pressed[k] = False
                if torque:
                    ks = synchronized(k)
                    if synchro == 0 or synchro == 1 or ks == k:
                        print('set',k,'to',values[k])
                        if degrees:
                            motors.setPositionDg(k,int(values[k]))
                        else:
                            motors.setPosition(k,int(values[k]))
                    if (synchro == 1 or synchro == -1) and ks != k:
                        print('set',ks,'to',values[k])
                        if degrees:
                            motors.setPositionDg(ks,int(values[k]))
                        else:
                            motors.setPosition(ks,int(values[k]))
                current = k
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
                currents = synchronized(current)
                if synchro == 0 or synchro == 1 or currents == current:
                    print('set',current,'to',newValue)
                    if degrees:
                        motors.setPositionDg(current,int(newValue))
                    else:
                        motors.setPosition(current,int(newValue))
                if (synchro == 1 or synchro == -1) and currents != current:
                    print('set',currents,'to',newValue)  
                    if degrees:
                        motors.setPositionDg(currents,int(newValue))
                    else:
                        motors.setPosition(currents,int(newValue))
    elif event == 'Units-Bin':
        degrees = False
        print('degrees off')
        for k in dofs:
            value = float(motors.dg2bin(k,values[k]))
            minVal, maxVal, _ = motors.getRange(k)
            window[k].update(range=(minVal, maxVal), value = value)
    elif event == 'Units-Degrees':
        degrees = True
        print('degrees on')
        for k in dofs:
            value = float(motors.bin2dg(k,values[k]))
            minVal, maxVal, _ = motors.getRangeDg(k)
            window[k].update(range=(minVal, maxVal), value = value)
    elif event == 'Torque-On':
        torque = True
        print('torque on')
        for k in dofs:
            motors.enableTorque(k)
    elif event == 'Torque-Off':
        torque = False
        print('torque off')
        for k in dofs:
            if concerned[k]:
                motors.disableTorque(k)
    elif event == 'Synchro-Off':
        synchro = 0
        print('synchronization off')
    elif event == 'Synchro-On':
        synchro = 1
        print('synchronization on')
    elif event == 'Synchro-Reverse':
        synchro = -1
        print('synchronization reverse')
    elif event == 'Mode-Pose':
        mode = True
        print('record pose')
        record = False
        replay = -1
        window["Stop Recording"].update(text="Next")
    elif event == 'Mode-Movement':
        mode = False
        print('record movement')
        record = False
        replay = -1
        window["Stop Recording"].update(text="Stop")
    elif event == "Period":
        period = int(values["Period"])
        if period < 10:
            period = 10
        elif period < 100:
            period = 10*(period//10)
        elif period < 1000:
            period = 100*(period//100)
        else:
            period = 500*(period//500)
        print('period updated to ',period)
        window["Period"].update(value=float(period))
        if period < 1000:
            beep = False
            window["beep"].update(value=False)
    elif event == "Save Recording" and values["Save Recording"] != '':
        filename = values["Save Recording"]
        with open(filename, 'w') as f:
            f.write(str(concerned_dofs)+'\n')  
            for r in recorded:
                f.write(str(r)+'\n')
        window["Save Recording"].update(value='')
        print('saved')
    elif event == "Load Recording" and values["Load Recording"] != '':
        filename = values["Load Recording"]
        recorded = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            concerned_dofs = eval(lines[0])
            for line in lines[1:]:
                r = eval(line[:-1])
                recorded.append(r)
            for k in dofs:
                concerned[k] = False
            for group in groups.keys():
                concern = False
                for k in concerned_dofs:
                    if k in groups[group]:
                        concern = True
                        break
                if concern:
                    for k in groups[group]:
                        concerned[k] = True
                window['concern-'+group].update(value=concern)
            change_current = False
            for k in concerned_dofs:
                if k == current:
                    change_current = False
                    break
                elif synchronized(k) == current:
                    change_current = True
            if change_current:
                current = synchronized(current)
        window["Captured"].update(value=str(len(recorded)))
        window["Load Recording"].update(value='')
        print('loaded')        
    elif 'Start Recording' in event:
        print('recording started')
        recorded = []
        concerned_dofs = [ k for k in dofs if concerned[k] ]
        window["Captured"].update(value="0")
        record = True
        replay = -1
        replaying = False
    elif 'Stop Recording' in event:
        if mode:
            print('record next')
            record = True
        else:
            print('recording stopped')
            record = False
        replay = -1
        replaying = False
    elif 'Replay Recording' in event:
        replaying = True
        print('replaying','one' if mode else 'many','...')
        if not torque:
            torque = True
            window["Torque-On"].update(value=True)
            for k in dofs:
                motors.enableTorque(k)
    elif event == "beep":
        beep = values["beep"]
        print('beep:',beep)
    elif "concern-" in event:
        for k in groups[event[8:]]:
            concerned[k] = values[event]
            if not values[event]:
                motors.enableTorque(k)
        recorded = []
        concerned_dofs = [ k for k in dofs if concerned[k] ]
        window["Captured"].update(value="0")
        record = False
        replay = -1
        replaying = False
    
    t1 = int(time.time()*1000/period)
    if t0 != t1:
        t0 = t1
        for k in dofs:
            position = motors.getPositionDg(k) if degrees else motors.getPosition(k)
            if not pressed[k]:
                window[k].update(value = position)
        if record:
            #print("recording", time.time(),t1)
            recorded.append([values[k] for k in dofs if concerned[k]] if degrees else [motors.bin2dg(k,values[k]) for k in dofs if concerned[k]])
            window["Captured"].update(value=str(len(recorded)))
            if beep:
                beeper.hear("C__") #print('\a')
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
                positions = { k:positionDg for positionDg, k in zip(recorded[replay],concerned_dofs) }
                if synchro == 1 or synchro == -1:
                    for k in concerned_dofs:
                        ks = synchronized(k)
                        if ks != k:
                            positions[ks] = positions[k]
                            if synchro == -1:
                                del positions[k]
                for k in positions.keys():
                    positionDg = positions[k]
                    motors.setPositionDg(k,positionDg)
                    if not pressed[k]:
                        window[k].update(value = position)
                if mode:
                    replaying = False
                    print('...replayed one')
        window["Replayed"].update(value=str(replay),visible=(replay != -1))
        
    left_frame, right_frame = cameras.read()
    left_fps, right_fps = cameras.fps()
    if left_frame is not None and left_fps > 1: 
        left_imgbytes = cv2.imencode(".png", cv2.resize(left_frame,(320,240)))[1].tobytes()
        window["Left-EYE"].update(data=left_imgbytes)
        window["Left-FPS"].update(value=str(left_fps)+" fps")
        if right_frame is None or right_fps <= 1:
            window["Right-EYE"].update(data=left_imgbytes)
            window["Right-FPS"].update(value="")
    if right_frame is not None and right_fps > 1:
        right_imgbytes = cv2.imencode(".png", cv2.resize(right_frame,(320,240)))[1].tobytes()
        window["Right-EYE"].update(data=right_imgbytes)
        window["Right-FPS"].update(value=str(right_fps)+" fps")

window.close()
motors.close()
cameras.close()
#os._exit(0)

