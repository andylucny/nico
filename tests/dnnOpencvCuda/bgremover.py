import numpy as np
import cv2

class bgremover:

    def __init__(self):
        # load model
        print("bgremover: loading model")
        modelPath = "modnet_webcam_portrait_matting_opset9.onnx"
        self.net = cv2.dnn.readNetFromONNX(modelPath)
        # select CPU or GPU
        #self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) #CPU
        #self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)      #CPU
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)    #GPU
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)      #GPU
        dummy = np.zeros((672,512,3),np.uint8)
        self.process(dummy)
        print("bgremover: model loaded")
        
    def process(self,frame):
        # load image
        blob = cv2.resize(frame,(672,512), cv2.INTER_AREA)
        blob = blob.astype(np.float)
        blob /= 255
        blob = 2*blob-1
        channels = cv2.split(blob)
        blob = np.array([[channels[2],channels[1],channels[0]]])

        # Sets the input to the network
        self.net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.net.forward()

        # Process the result
        mask = outs[0][0]
        mask = cv2.resize(mask,(frame.shape[1],frame.shape[0]))
        mask = cv2.merge([mask,mask,mask])
        result = (mask * frame + (1-mask)*np.ones_like(frame)*255).astype(np.uint8)
        mask = (mask*255).astype(np.uint8)
        
        return result, mask
