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
degrees = False

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
            sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key='read-'+key),
        ])
    return layout
    
def update_side_layout(layout, kind='Left', id=0): #id=10
    for i in range(10):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        layout[0][id//5].Rows[i+1][1].Update(range=(minVal, maxVal),value=defVal)

def addons_layout(id=20):
    layout = [
        [ sg.Text("Units", size=(10, 1)), sg.Radio("Bins", "Units", True, size=(10, 1)), sg.Radio("Degrees", "Units", False, size=(10, 1)) ],
        [ sg.Text("Torque", size=(10, 1)), sg.Radio("Off", "Torque", True, size=(10, 1)), sg.Radio("On", "Torque", False, size=(10, 1)) ]
    ]
    texts = ["Neck up-down","Neck left-right"]
    for i in range(2):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        layout.append([ sg.Text(texts[i], size=(10, 1))])
        layout.append([ sg.Slider((minVal, maxVal), defVal, 1, orientation="h", size=(slider_v, slider_h), key='read-'+key)])
    layout.append([ sg.VPush() ])
    layout.append([ sg.Push(), sg.Button("Exit", size=(10, 1)) ])
    return layout
    
def update_addons_layout(layout, id=20):
    for i in range(2):
        key = dofs[id+i]
        minVal, maxVal, defVal = motors.getRangeDg(key) if degrees else motors.getRange(key)
        print('update',minVal, maxVal, defVal)
        layout[0][4].Rows[3+2*i][0].Update(range=(minVal, maxVal),value=defVal)
    
layout = [[
    sg.Column(side_layout('Left',0), vertical_alignment='top'), 
    sg.VSeparator(),
    sg.Column(side_layout('Right',10), vertical_alignment='top'),      
    sg.VSeparator(),
    sg.Column(addons_layout(20), vertical_alignment='top', expand_y=True)   
]]

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
fps = 30 
cap.set(cv2.CAP_PROP_FPS,fps)    

# Create the window and show it without the plot
window = sg.Window("Nico control GUI", layout, finalize=True)

window.bind("<Escape>", "Exit")

t0 = int(time.time())
last_values = None
torque = False
for k in dofs:
    motors.disableTorque(k)
while True:
    event, values = window.read(timeout=20)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

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
                    update_side_layout(layout,'Left',0)
                    update_side_layout(layout,'Right',10)
                    update_addons_layout(layout,20)
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
                elif isinstance(k, str) and 'read-' in k:
                    if torque:
                        print('set',k[5:],'to',values[k])
                        if degrees:
                            motors.setPositionDg(k[5:],int(values[k]))
                        else:
                            motors.setPosition(k[5:],int(values[k]))
        last_values = values

    t1 = int(time.time())
    if t0 != t1:
        for k in dofs:
            position = motors.getPositionDg(k) if degrees else motors.getPosition(k)
            window['read-'+k].update(value = position)
            last_values['read-'+k] = float(position)
            
    _, frame = cap.read()
    if frame is not None:
        imgbytes = cv2.imencode(".png", cv2.resize(frame,(320,240)))[1].tobytes()
        window["Left-EYE"].update(data=imgbytes)
        window["Right-EYE"].update(data=imgbytes)

window.close()

