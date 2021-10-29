import numpy as np
import cv2

class faceRecognizer:

    def __init__(self):
        print("faceRecognizer: loading model")
        # load model
        self.net = cv2.dnn.readNetFromTensorflow('VGGFace2.pb')
        face = cv2.imread('Andy.jpg')
        self.andy = None
        _, self.andy = self.process(face,face)
        print("faceRecognizer: model loaded")
        
    def process(self,image,face):
        # vectorize face 
        height = 224
        width = 224
        mean = (93.5940,104.7624,129.1863)

        # blob preparation
        blob = cv2.dnn.blobFromImage(face,1.0,(width,height),mean)

        # use network
        self.net.setInput(blob)
        vector = self.net.forward()
        
        result = np.copy(image)
        if self.andy is not None:
            distance = np.linalg.norm(vector-self.andy)
            print(distance)
            limit = 105
            text = "unknown"
            if distance < limit:
                text = "Andy"

            cv2.putText(result, text, (25, 25), 0, 1.0, (255, 255, 255), 2)
                

        return result, vector

