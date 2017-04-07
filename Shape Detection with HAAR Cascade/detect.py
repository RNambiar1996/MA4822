import numpy as np
import cv2


plus_cascade = cv2.CascadeClassifier('cascade.xml')

img = cv2.imread("test-1.jpg")
img = cv2.resize(img, (100,100))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
# add this
# image, reject levels level weights.
detections = plus_cascade.detectMultiScale(gray, 50, 50)
    
# add this
for (x,y,w,h) in detections:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


cv2.imshow('img',img)
cv2.waitKey()

cv2.destroyAllWindows()
