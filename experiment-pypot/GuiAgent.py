import PySimpleGUI as sg
from agentspace import Agent, space, Trigger
import numpy as np
import cv2
import time
import os
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
                sg.Text("Name", size=(10, 1)), 
                sg.Input("", size=(25, 1), key="Name"), 
            ],
            [ 
                sg.Text("Head", size=(10, 1)), 
                sg.Radio("Off", "Head", False, size=(8, 1), key="Head-off", enable_events=True), 
                sg.Radio("On", "Head", True, size=(8, 1), key="Head-on", enable_events=True) 
            ],
            [
                sg.Button("Run", size=(10, 1)),
                sg.Button("Stop", size=(10, 1)),
                sg.Button("Exit", size=(10, 1)),
            ],
        ]
        window = sg.Window("Experiment", layout, finalize=True)
        window.bind("<Return>", "Stop")
        blank = np.zeros((240,320,3),np.uint8)
        head = True
        while True:
            event, values = window.read(timeout=10)
            if event != "__TIMEOUT__":
                print(event)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Head-off":
                head = False
                space["head"] = head
            elif event == "Head-on":
                head = True
                space["head"] = head
            elif event == "Run":
                space["experiment"] = True
            elif event == "Stop":
                if space(default=False)["experiment"]:
                    space["stop"] = True
                    print("Stop button pressed")
            
            if "Name" in values.keys():
                if space(default="")["name"] != values["Name"]:
                    space["name"] = values["Name"]
                    print("name",space["name"])
                    
            robot_img = space(default=blank)['robotImage']
            robot_imgbytes = cv2.imencode(".png", cv2.resize(robot_img,(320,240)))[1].tobytes()
            window["robotImage"].update(data=robot_imgbytes)
            human_img = space(default=blank)['humanImage']
            human_imgbytes = cv2.imencode(".png", cv2.resize(human_img,(320,240)))[1].tobytes()
            window["humanImage"].update(data=human_imgbytes)

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
