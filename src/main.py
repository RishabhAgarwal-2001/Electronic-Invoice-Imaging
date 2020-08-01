from Text_Localization.text_localization import localTextRegion
from Table_Start_Detection.detect_table import detectTable
from Table_Start_Detection.crop_table import cropTable
import cv2

fileName = 'im7_full.png'

# Detecting and Separating MetaData and Table out of the invoice Image
print("Startied Process....")
print("Table and Meta Data Separation Started...")
tablePosition = detectTable(fileName)
image = cv2.imread('../images/'+fileName)
cropTable(image, tablePosition)
print("Table and Meta Data Separation Completed!!!\n\n")

# Reading in the metaData and Table Image
path_to_meta_data = '../results/table_meta_data/metaData.png'
path_to_table = '../results/table_meta_data/table.png'
metaData = cv2.imread(path_to_meta_data)
table = cv2.imread(path_to_table)

# Separating Meta Data Regions
obj = localTextRegion(metaData)