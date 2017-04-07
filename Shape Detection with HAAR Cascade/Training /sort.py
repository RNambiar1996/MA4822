import cv2
import os
import glob 

input_path = raw_input("Enter path directory to images to sort: ")
output_path = raw_input("Directory to store images: ")

cnt = int(raw_input("Starting number: "))

for im_path in glob.glob(os.path.join(input_path, "*")):
	img = cv2.imread(im_path)

	if img is not None: 
		img = cv2.resize(img, (100,100))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		cv2.imshow("Image", img)
		cv2.waitKey(1)
		cmd = raw_input("y/n: ")
		if str(cmd) == "y":
			cv2.imwrite(str(output_path) + "/img " + str(cnt) + ".png", img)
			cnt += 1
		
