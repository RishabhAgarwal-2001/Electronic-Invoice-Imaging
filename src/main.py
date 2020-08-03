from Text_Localization.text_localization import localTextRegion
from Table_Start_Detection.detect_table import detectTable
from Table_Start_Detection.crop_table import cropTable
from Deskew.deskewImage import deskewImage
import cv2
from Text_Detection.detect_text import convert_crops_to_text
from Line_Detection.EdgeDetectionAll import EdgeDetectionAll

fileName = 'im7_full.png'

# Deskewing Image
print("Started Process....")
print("Deskewing Image....")
image = cv2.imread('../images/'+fileName)
deskewImage(image)
print("Deskewing Completed!!!")


# Detecting and Separating MetaData and Table out of the invoice Image
print("Table and Meta Data Separation Started...")
tablePosition = detectTable(fileName)
image = cv2.imread('../results/deskew_image/image.png')
cropTable(image, tablePosition)
print("Table and Meta Data Separation Completed!!!\n\n")


# Reading in the metaData and Table Image
path_to_meta_data = '../results/table_meta_data/metaData.png'
path_to_table = '../results/table_meta_data/table.png'
metaData = cv2.imread(path_to_meta_data)
table = cv2.imread(path_to_table)

# Cropping Based on Lines
print("Cropping Based on Horizontal And Vertical Lines...")
EdgeDetectionAll(path_to_meta_data, False)
print("Completed!!!")

# Separating Meta Data Regions
obj = localTextRegion(metaData)

# Converting Crops into text
convert_crops_to_text()