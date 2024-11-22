import os
import io
import requests
import zipfile
import numpy as np
import cv2
import onnxruntime as ort
import time

def download_zipfile(path,url):
    if os.path.exists(path):
        return
    print("downloading",url)
    response = requests.get(url)
    if response.ok:
        file_like_object = io.BytesIO(response.content)
        zipfile_object = zipfile.ZipFile(file_like_object)    
        zipfile_object.extractall(".")
    print("downloaded")
    
def download_nico_touch_model():
    download_zipfile('nico-touch-right-arm.onnx','http://www.agentspace.org/download/nico-touch.zip')

#download_nico_touch_model()

providers = ['CPUExecutionProvider']
touch_model = ort.InferenceSession('nico-touch-right-arm.onnx', providers=providers)

def points2postures(points, resolution):
    inp = np.array(points,np.float32) / np.array([resolution],np.float32)
    out = touch_model.run(None, {"input": inp})[0]
    postures = []
    for posture, inp_i in zip(out, inp):
        if posture[3] > 1.0: # elbow
            posture[3] = 1.0 # not possible to reach
        if posture[5] > 1.0: # wrist-x
            posture[5] = 1.0
        posture = list(np.round(posture[:6]*180)) + [ round((inp_i[0]-0.5)*35), round((inp_i[1]-0.5)*5)-30 ]
        postures.append(posture)
    return postures

labels = []
points = []
with open('points-on-touchscreen.txt','r') as f:
    for line in f.readlines()[1:]:
        record = eval(line)
        labels.append(record[0])
        points.append(record[1:3])

postures = points2postures(points, resolution=(2400, 1350))

data = { label:posture for label, posture in zip(labels, postures) }

with open('angles-on-touchscreen.txt','wt') as g:
    g.write("['label', 'r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x']\n")
    for i in range(1,8):
        g.write(str([i]+data[i])+'\n')
