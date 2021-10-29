# import the necessary packages
import numpy as np
import cv2

class faceDetector:

    def __init__(self):
        print("faceDetector: loading model")
        # defining prototext and caffemodel paths
        caffeModel = "res10_300x300_ssd_iter_140000.caffemodel"
        prototextPath = "deploy.prototxt"
        # Load Model
        self.net = cv2.dnn.readNetFromCaffe(prototextPath,caffeModel)
        dummy = np.zeros((300,300,3),np.uint8)
        self.process(dummy)
        print("faceDetector: model loaded")

    def process(self,image):
        height = 300
        width = 300
        mean = (104.0, 177.0, 123.0)
        threshold = 0.5
        h, w = image.shape[:2] 

        # convert to RGB
        rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        # blob preparation
        blob = cv2.dnn.blobFromImage(cv2.resize(image,(width,height)),1.0,(width,height),mean)

        # passing blob through the network to detect and pridiction
        self.net.setInput(blob)
        detections = self.net.forward()

        # loop over the detections
        rects = []
        face = None
        for i in range(detections.shape[2]):
            # extract the confidence and prediction
            confidence = detections[0, 0, i, 2]
            # filter detections by confidence greater than the minimum
            if confidence > threshold:
                # compute the (x, y)-coordinates of the bounding box for the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype(np.int)
                rects.append((startX, startY, endX, endY, confidence))
                if face is None:
                    face = np.copy(image[startY:endY,startX:endX,:])

        result = np.copy(image)
        for rect in rects:
            startX, startY, endX, endY, confidence = rect
            cv2.rectangle(result, (startX, startY), (endX, endY), (0, 0, 255), 2)
            text = "{:.2f}%".format(confidence * 100)
            cv2.putText(result, text, (startX, startY-5), 0, 1.0, (0, 0, 255), 2)

        return result, face
