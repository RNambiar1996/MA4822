import cv2
import os
import glob 

input_path = raw_input("Enter path directory to images to sort: ")
output_path = raw_input("Directory to store images: ")

cnt = int(raw_input("Starting number: "))
w = int(raw_input("Width: "))
h = int(raw_input("Height: "))

for im_path in glob.glob(os.path.join(input_path, "*")):
	img = cv2.imread(im_path)

	if img is not None: 
		img = cv2.resize(img, (w,h))
		cv2.imwrite(str(output_path) + "/img " + str(cnt) + ".png", img)
		cnt += 1
		
