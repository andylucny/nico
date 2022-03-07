import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import easyocr
reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
result = reader.readtext('chinese.jpg')

import cv2
image = cv2.imread('chinese.jpg')
result2 = reader.readtext(image)

for res in result2:
    points = res[0]
    for i in range(len(points)):
        j = (i+1) % len(points)
        cv2.line(image,points[i],points[j],(0,0,255),2)
    
cv2.imshow('text',image)
cv2.waitKey(0)
