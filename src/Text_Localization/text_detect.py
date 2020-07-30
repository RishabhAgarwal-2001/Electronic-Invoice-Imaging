import pytesseract
from pytesseract import Output
import cv2
import numpy as np


def text_detect(img):
	d = pytesseract.image_to_data(img, output_type=Output.DICT)
	n_boxes = len(d['level'])
	image_area = img.shape[0] * img.shape[1]
	valid_boxes = []
	for i in range(n_boxes):
	    box_area = d['width'][i]*d['height'][i]
	    if(0.98*image_area<box_area):
	    	continue
	    text = d['text'][i].lstrip()
	    text = text.rstrip()
	    if(text==''):
	        continue
	    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	    valid_boxes.append([x, y, w, h])
	    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	mask = np.zeros(shape=img.shape, dtype=np.uint8)
	for bbox in valid_boxes:
		(x, y, w, h) = bbox
		cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), thickness=cv2.FILLED)

	return mask, img