from easyocr import Reader
import numpy as np
import cv2

def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 256 else "" for c in text]).strip()

class textDetector:

    def __init__(self):
        print("textDetector: loading model")
        # OCR the input image using EasyOCR
        langs = ["en", "sk"]
        self.reader = Reader(langs, gpu=True)
        print("textDetector: model loaded");
        
    def process(self,frame):
        results = self.reader.readtext(frame)

        image = np.copy(frame)
        # loop over the results
        for (bbox, text, prob) in results:
            # unpack the bounding box
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            # cleanup the text and draw the box surrounding the text along
            # with the OCR'd text itself
            text = cleanup_text(text)
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            cv2.putText(image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        return image
