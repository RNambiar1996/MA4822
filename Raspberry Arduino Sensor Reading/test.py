import cv2
import time

cap = cv2.VideoCapture(0)

while cap.isOpened():
	print "Hello"
	ret,image = cap.read()
	
	if ret is not None:
		cv2.imshow("IMage", image)
		cv2.waitKey(1)
