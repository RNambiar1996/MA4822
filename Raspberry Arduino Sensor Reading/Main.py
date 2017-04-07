import serial 
import time
import numpy as np
from matplotlib import pyplot as plt
import cv2
import socket 
import struct
import pickle
import math

#from shapeDetector import ShapeDetector

plt.axis([0,1000,0,100])

def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)

def main():
	
	output_text = open("ouput.txt", "w")
	

	#dictionary of all contours
	contours = {}
	#array of edges of polygon
	approx = []
	#scale of the text
	scale = 2
	#camera

	filter = raw_input("Color: ")
	
	if str(filter) == "red": 	
		lower = [0,150,0]
		upper = [5,255,255]
		lower = np.array(lower, dtype = np.uint8)	
		upper = np.array(upper, dtype = np.uint8)
	
	elif str(filter) == "blue":
		sensitivity_blue = 20
		lower=np.array([120-sensitivity,150,0],np.uint8)
		upper=np.array([120+sensitivity,255,255],np.uint8)

	elif str(filter) == "green":
		#sensitivity_green = 5;
		lower = [29, 86, 6]  # lower bound
		upper = [64, 255, 255] #upper bound		
		lower = np.array(lower, dtype = np.uint8)
		upper = np.array(upper, dtype = np.uint8)
	

	
	#start time
	start = time.time()
	#counter for x axis of dyanmic plot	
	x = 0

	#initiating serial to communicate with arduino at bauda rate of 9600
	arduino = serial.Serial("/dev/ttyACM0", 9600)

	#Labels for dyanmic plot
	plt.ylabel("Distance")
	plt.xlabel("Time")

	detected = 0
	counter = 0
	
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect(('localhost', 9999))

	#initiate camera 
	cap = cv2.VideoCapture(0)
	
	arduino.write("Start")
	#loop
	while cap.isOpened():
		
		shape = "UNKNOWN"
		
		#reading arduino data sent over serial	
		mic = arduino.readline().rstrip()
		print "Sound level: ", mic
		output_text.write("Audio level: " + str(mic))
		output_text.write("\n")
			
		
		ultrasound = arduino.readline().rstrip()
		print "ultrasound: ", ultrasound
		output_text.write("Ultrasound reading: " + str(ultrasound))
		output_text.write("\n") 
		#removing end of line characters
		#try:
		#	ultrasound = int(ultrsound.rstrip())
		#	print("Distance to object: ", ultrasound)
		#	print "\n"

		#except:
		#	ultrasound = 0
		#	print " Ultrsound Error"
		#	print "\n"

		
		pot = arduino.readline().rstrip()
		print "Potentiometer: ", pot
		output_text.write("Potentiometer reading: " + str(pot))
		output_text.write("\n")
	
		
		temp = arduino.readline().rstrip()
		print "Temp: ", temp
		output_text.write("Temperature reading: " + str(temp))
		output_text.write("\n")

		
		
		#plotting data 
		
		try:
			plt.scatter(x, ultrasound)
			x += 1
			plt.pause(0.001)
		
		except: 
			print "error"
		
		
		ret, frame = cap.read()
		#if image is read from camera
		
		if ret is True:
		
			#grayscale
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			mask = cv2.inRange(hsv, lower, upper)
			output = cv2.bitwise_and(hsv, hsv, mask = mask)

			gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
			_, thresh = cv2.threshold(gray, 127, 255, 0)
				
			#Canny
			canny = cv2.Canny(thresh,80,240,3)

			#contours
			canny2, contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			for i in range(0,len(contours)):
			    #approximate the contour with accuracy proportional to
			    #the contour perimeter
			    approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)

			    #Skip small or non-convex objects
			    if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
				continue

			    #triangle
			    if(len(approx) == 3):
				x,y,w,h = cv2.boundingRect(contours[i])
				shape = "Triangle"
				cv2.putText(frame,'TRI',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
				detected = 1
				cv2.drawContours(frame, contours[i], -1, (0,255,0), 2)
			    elif(len(approx)>=4 and len(approx)<=6):
				#nb vertices of a polygonal curve
				vtc = len(approx)
				#get cos of all corners
				cos = []
				for j in range(2,vtc+1):
				    cos.append(angle(approx[j%vtc],approx[j-2],approx[j-1]))
				#sort ascending cos
				cos.sort()
				#get lowest and highest
				mincos = cos[0]
				maxcos = cos[-1]

				#Use the degrees obtained above and the number of vertices
				#to determine the shape of the contour
				x,y,w,h = cv2.boundingRect(contours[i])
				cv2.drawContours(frame, contours[i], -1, (0,255,0), 2)
				if(vtc==4):
				    shape = "Square"
				    cv2.putText(frame,'RECT',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
				    detected = 1
				elif(vtc==5):
				    shape = "Pentagon"
				    cv2.putText(frame,'PENTA',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
				    detected = 1
				elif(vtc==6):
				    shape = "Hexagon"
				    cv2.putText(frame,'HEXA',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
				    detected = 1
			    else:
				#detect and label circle
				area = cv2.contourArea(contours[i])
				x,y,w,h = cv2.boundingRect(contours[i])
				radius = w/2
				if(abs(1 - (float(w)/h))<=2 and abs(1-(area/(math.pi*radius*radius)))<=0.2):
				    shape = "Circle"
				    cv2.putText(frame,'CIRC',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
				    cv2.drawContours(frame, contours[i], -1, (0,255,0), 2)
				    detected = 1

			if(detected == 1):
				#cv2.imwrite("Detection" +str(counter) + ".png", frame)
				#output_file.write("Detected " +str(shape) + " at " +str(x) +","+str(y))			
				counter += 1
				detected = 0

			#Display the resulting frame
			#out.write(frame)
			cv2.imshow('frame',frame)
			cv2.imshow('canny',canny)
			if cv2.waitKey(1) == 1048689: #if q is pressed
				cap.release()			   
				break

			#compressing data
			data = pickle.dumps(frame)
			#sending data over socket
			clientsocket.sendall(struct.pack("L", len(data)) + data)
				
	
if __name__ == "__main__":
	main()
		
	

