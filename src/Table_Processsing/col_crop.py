import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def sort_contours(cnts, method="left-to-right"):
    reverse=False
    i=0
    if method=="right-to-left" or method=="bottom-to-top":
      reverse=True

    if method=="top-to-bottom" or method=="bottom-to-top":
      i=1
    boundingBoxes=[cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes)=zip(*sorted(zip(cnts, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))

    return (cnts, boundingBoxes)

file=r'F:\Vacation_TP\D2C_Flipkart\Electronic Invoicing using Image Processing\Sample Invoices\Capture.PNG'
img=cv2.imread(file)
print(img.shape)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray=255-gray
ver_kernel_er=cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
hor_kernel_er=cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
gray2=cv2.erode(gray,hor_kernel_er)
gray2=cv2.dilate(gray2,hor_kernel_er)
gray3=cv2.erode(gray,ver_kernel_er)
gray3=cv2.dilate(gray3,ver_kernel_er)

img_534=cv2.addWeighted(gray2, 0.5, gray3, 0.5, 0.0)


cv2.imshow("Yeh waala",img_534)

edges = cv2.Canny(img_534, 75, 150)

kernel_6x6=cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
edges6=cv2.dilate(edges,kernel_6x6)
edges6=cv2.erode(edges6,kernel_6x6)

cv2.imshow("linesEdges6x6", edges6)
vlines=[]
hlines=[]
lines = cv2.HoughLinesP(edges6, 0.1, np.pi/2, 10, maxLineGap=30)
for line in lines:        
    x1, y1, x2, y2 = line[0]
    if x1==x2:
        vlines.append([x1,y1,x2,y2])
    else:
        hlines.append([x1,y1,x2,y2])
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 128), 1)


cv2.imshow("linesDetected", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

vlines.sort(key = lambda x: x[0])

top=hlines[0][1]

counter=1
for i in range(1,len(vlines)):
    line=vlines[i]
    line_prev=vlines[i-1]
    if(line[0]-line_prev[0]<5):
        continue
    imcrop=img[top:582,line_prev[0]:line[0]]
    cv2.imshow("Crop",imcrop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    crop_folder = r'F:\Vacation_TP\D2C_Flipkart\Electronic Invoicing using Image Processing\crops'
    cropName = crop_folder + "Crop_" + str(counter) + ".jpg"
    counter = counter + 1 
    cv2.imwrite(cropName, imcrop)
