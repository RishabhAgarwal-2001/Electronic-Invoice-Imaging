import sys
import PIL.ImageOps
from PIL import Image
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


file=r'F:\Vacation_TP\D2C_Flipkart\Electronic Invoicing using Image Processing\Sample Invoices\Capture_SI_8.png'
img=cv2.imread(file)
im_og=img.copy()


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


# cv2_imshow(img_534)

edges = cv2.Canny(img_534, 75, 150)

kernel_6x6=cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
edges6=cv2.dilate(edges,kernel_6x6)
edges6=cv2.erode(edges6,kernel_6x6)

# cv2_imshow(edges6)
vlines=[]
hlines=[]
lines = cv2.HoughLinesP(edges6, 0.1, np.pi/2, 10, maxLineGap=30)
for line in lines:        
    x1, y1, x2, y2 = line[0]
    if x1==x2 and (y1<(img.shape[1])/3 or y2<(img.shape[1])/3 ) :
        vlines.append([x1,y1,x2,y2])
    else:
        hlines.append([x1,y1,x2,y2])
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 128), 1)


# cv2_imshow(img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

vlines.sort(key = lambda x: x[0])
hlines.sort(key = lambda x: x[1])

top=hlines[0][1]
# cv2_imshow(im_og)
counter=1
for i in range(1,len(vlines)):
    line=vlines[i]
    line_prev=vlines[i-1]
    if(line[0]-line_prev[0]<5):
        continue
    imcrop=im_og[top:img.shape[0],line_prev[0]-5:line[0]+5]
    imcrop = cv2.cvtColor(imcrop, cv2.COLOR_BGR2GRAY)

    # print(imcrop)
    # cv2_imshow(imcrop)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    crop_folder = r'Electronic Invoicing using Image Processing\crops'
    cropName = crop_folder + "Crop_" + str(counter) + ".png"
    counter = counter + 1 
    cv2.imwrite(cropName, imcrop)

crop_list=[]
for icrtr in range (1,counter):
    crop_list.append(crop_folder + "Crop_" + str(icrtr) + ".png")

print(crop_list)

# images = [Image.open(x) for x in ['Crop_1.png', 'Crop_2.png', 'Crop_3.png', 'Crop_4.png', 'Crop_5.png', 'Crop_6.png', 'Crop_7.png', 'Crop_8.png', 'Crop_9.png', 'Crop_10.png']]
images = [Image.open(x) for x in crop_list]

widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)+counter*20
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 20
for im in images:
  im1=PIL.ImageOps.invert(im)
  new_im.paste(im1, (x_offset,20))
  x_offset += im1.size[0] + 20

new_im=PIL.ImageOps.invert(new_im)

new_im.save('test_inv_8.jpg')
print("Done")
