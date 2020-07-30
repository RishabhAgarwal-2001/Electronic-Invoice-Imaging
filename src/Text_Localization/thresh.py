import cv2
import numpy as np


def thresh(Image, org_image):

	# Applying imclose
	kernel = np.ones((31, 31), np.uint8)
	Image = cv2.morphologyEx(Image, cv2.MORPH_CLOSE, kernel)

	# Converting image in hsv and applying threshold
	hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
	lower = np.array([0, 0, 218])
	upper = np.array([157, 54, 255])
	mask = cv2.inRange(hsv, lower, upper)





	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	dilate = cv2.dilate(mask, kernel, iterations=30)


	# Analyze the results
	# cv2.imshow("This", dilate)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

	#cnts = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	boundingBoxes = []

	for c in cnts:
	    x,y,w,h = cv2.boundingRect(c)
	    boundingBoxes.append([x,y,w,h])
	    cv2.rectangle(org_image, (x, y), (x+w, y+h), (255, 0, 255), 2)    

	return dilate, org_image, boundingBoxes
