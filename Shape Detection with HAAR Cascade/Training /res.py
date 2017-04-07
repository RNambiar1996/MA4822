import cv2

img = cv2.imread("img.png", 0)

img = cv2.resize(img, (20, 20))

cv2.imwrite("img_2.png", img)
