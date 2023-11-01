import PySimpleGUI as sg
from agentspace import Agent, space, Trigger
import numpy as np
import cv2
import time
import os
from datetime import datetime
from ExperimentAgent import close

class GuiAgent(Agent):
      
    def init(self):
        #GUI
        layout = [
            [
                sg.Image(filename="", key="humanImage"),
                sg.Image(filename="", key="robotImage")
            ],
            [
                sg.Image(filename="", key="robotEye"),
                sg.Image(filename="", key="touchImage")
            ],
            [ 
                sg.Text("Name", size=(13, 1)), 
                sg.Input("", size=(25, 1), key="Name"), 
            ],
            [ 
                sg.Text("Show intention", size=(13, 1)), 
                sg.Radio("Off", "ShowIntention", True, size=(8, 1), key="ShowIntention-off", enable_events=True), 
                sg.Radio("On", "ShowIntention", False, size=(8, 1), key="ShowIntention-on", enable_events=True),
                sg.Text("      ", size=(5, 1)), 
                sg.Text("Tell instructions", size=(13, 1)), 
                sg.Radio("Off", "TellIstructions", True, size=(8, 1), key="TellIstructions-off", enable_events=True), 
                sg.Radio("On", "TellIstructions", False, size=(8, 1), key="TellIstructions-on", enable_events=True) 
            ],
            [ 
                sg.Text("Stop mode", size=(13, 1)), 
                sg.Radio("Button", "StopMode", False, size=(8, 1), key="StopMode-button", enable_events=True), 
                sg.Button("Stop", size=(8, 1)),
                sg.Radio("40%", "StopMode", True, size=(8, 1), key="StopMode-40", enable_events=True),
                sg.Radio("50%", "StopMode", False, size=(8, 1), key="StopMode-50", enable_events=True),
                sg.Radio("60%", "StopMode", False, size=(8, 1), key="StopMode-60", enable_events=True),
                sg.Radio("65%", "StopMode", False, size=(8, 1), key="StopMode-65", enable_events=True),
                sg.Radio("80%", "StopMode", False, size=(8, 1), key="StopMode-80", enable_events=True)
            ],
            [ 
                sg.Text("Head", size=(13, 1)), 
                sg.Radio("Off", "Head", False, size=(8, 1), key="Head-off", enable_events=True), 
                sg.Radio("On", "Head", True, size=(8, 1), key="Head-on", enable_events=True) 
            ],
            [
                sg.Text("Duration", size=(8, 1), justification="left"),
                sg.Slider((1,10), 4, 1, orientation="h", size=(20, 10), key='Duration', enable_events=True),
                sg.Text("s", size=(2, 1), justification="left"),
            ],
            [
                sg.Slider((1,100), 1, 1, orientation="h", size=(20, 10), key='MaxCount', enable_events=True),
                sg.Text("x", size=(2, 1), justification="left"),
                sg.Button("Run", size=(10, 1)),
                sg.Button("Exit", size=(10, 1))
            ],
        ]
        window = sg.Window("Experiment", layout, finalize=True)
        window.bind("<Return>", "Stop")
        window.bind("<Up>","Run")
        window.move(50,10)
        #blank = np.zeros((240,320,3),np.uint8)
        blank = np.zeros((360,480,3),np.uint8)
        #blank = np.zeros((480,640,3),np.uint8)
        lastExperimentState = False
        while True:
            event, values = window.read(timeout=10)
            if event != "__TIMEOUT__":
                print(event)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "ShowIntention-off":
                space["ShowIntention"] = False
            elif event == "ShowIntention-on":
                space["ShowIntention"] = True
            elif event == "TellIstructions-off":
                space["TellIstructions"] = False
            elif event == "TellIstructions-on":
                space["TellIstructions"] = True
            elif event.startswith("StopMode-"):
                option = event[len("StopMode-"):]
                percentage = int(option) if option != "button" else 0
                space["StopMode"] = percentage
            elif event == "Head-off":
                space["head"] = False
            elif event == "Head-on":
                space["head"] = True
            elif event == "Run":
                space["experiment"] = True
            elif event == "Stop":
                if space(default=False)["experiment"]:
                    space["stop"] = True
                    print("Stop button pressed")
            elif event =="Duration":
                if "Duration" in values.keys():
                    duration = int(values["Duration"])
                    space["Duration"] = duration
                    print("Duration = ",duration)
            elif event == "MaxCount":
                if "MaxCount" in values.keys():
                    maxcount = int(values["MaxCount"])
                    space["MaxCount"] = maxcount
                    print("MaxCount = ",maxcount)
            
            if "Name" in values.keys():
                if space(default="")["name"] != values["Name"]:
                    space["name"] = values["Name"]
                    print("name",space["name"])
                    
            robot_img = space(default=blank)['robotImage']
            robot_imgbytes = cv2.imencode(".png", cv2.resize(robot_img,(blank.shape[1],blank.shape[0])))[1].tobytes()
            window["robotImage"].update(data=robot_imgbytes)
            human_img = space(default=blank)['humanImage']
            human_imgbytes = cv2.imencode(".png", cv2.resize(human_img,(blank.shape[1],blank.shape[0])))[1].tobytes()
            window["humanImage"].update(data=human_imgbytes)
            robot_eye = space(default=blank)['robotEye']
            robot_eyebytes = cv2.imencode(".png", cv2.resize(robot_eye,(blank.shape[1],blank.shape[0])))[1].tobytes()
            window["robotEye"].update(data=robot_eyebytes)
            robot_touch = np.copy(space(default=blank)['touchImage'])
            robot_touch_resized = cv2.resize(robot_touch,(blank.shape[1],blank.shape[0]))
            cv2.putText(robot_touch_resized,str(datetime.now())[:22],(10,robot_touch_resized.shape[0]-15),0,1.0,(255,255,255),1)
            count = space(default=0)["count"]
            if count > 0:
                cv2.putText(robot_touch_resized,'#'+str(count),(10,28),0,1.0,(255,255,255),1)
            robot_touchbytes = cv2.imencode(".png", robot_touch_resized)[1].tobytes()
            window["touchImage"].update(data=robot_touchbytes)
            
            experimentState = space(default=False)["experiment"]
            if experimentState != lastExperimentState:
                window["Run"].update(disabled=experimentState)
                lastExperimentState = experimentState

        window.close()
        Agent.stopAll()
        close()
        print('exiting')
        os._exit(0)
               
    def senseSelectAct(self):
        pass

if __name__ == "__main__":
    class MonitoringAgent(Agent):
          
        def init(self):
            space.attach_trigger("experiment",self,Trigger.NAMES)
            space.attach_trigger("head",self,Trigger.NAMES)
            space.attach_trigger("stop",self,Trigger.NAMES)
            space.attach_trigger("name",self,Trigger.NAMES)
        
        def senseSelectAct(self):
            name = self.triggered()
            print('space',name,space[name] if name is not None else "")

    GuiAgent()
    MonitoringAgent()
    time.sleep(1)
    space['robotImage'] = np.ones((480,640,3),np.uint8)*100
    space['humanImage'] = np.ones((480,640,3),np.uint8)*180
