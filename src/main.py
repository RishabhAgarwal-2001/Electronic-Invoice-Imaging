from Text_Localization.text_localization import localTextRegion
from Table_Start_Detection.detect_table import detectTable
from Table_Start_Detection.crop_table import cropTable
from Deskew.deskewImage import deskewImage
import cv2
from Text_Detection.detect_text import convert_crops_to_text
from Line_Detection.EdgeDetectionAll import EdgeDetectionAll
from Generate_Data.generate_data import GenerateData
from Key_Value.findValue import *
import xlwt

fileName = 'im11_full.png'

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
print("Table and Meta Data Separation Completed!!!\n")


# Reading in the metaData and Table Image
path_to_meta_data = '../results/table_meta_data/metaData.png'
path_to_table = '../results/table_meta_data/table.png'
metaData = cv2.imread(path_to_meta_data)
table = cv2.imread(path_to_table)

# Cropping Based on Lines
print("Cropping Meta Data Image Based on Horizontal And Vertical Lines...")
EdgeDetectionAll(path_to_meta_data, False)
print("Completed!!!")

# Separating Meta Data Regions
obj = localTextRegion(metaData)

# Converting Crops into text
convert_crops_to_text()

folder = '../results/crops_localization/'
print("Generating Data...")
lst = GenerateData(folder)
# print(lst)
print("Finding Values...")
finalDict = findValues(lst)
finalDict.update(FindPONumber(lst))
finalDict.update(FindInvNumber(lst))
dateList = ['LR', 'INVOICE', 'DA', 'DELIVERY', 'PURCHASE', 'PO', 'DUE', 'LOA', 'ORDER', 'PICKING', 'PASS', 'CHALLAN', 'DISPATCH', 'SO', 'DATED']
finalDict.update(FindDate(lst, dateList))
finalDict.update(FindCurrency(lst))
print("Final Dictionary: ",finalDict)

print("Creating Excel Sheet...")
wb = xlwt.Workbook()
ws = wb.add_sheet('Invoice Sheet')
row = 0
column = 0
for i in finalDict.keys():
    ws.write(row, column, i)
    ws.write(row, column+1, finalDict[i])
    row += 1
wb.save('Invoice_Sheet.xlsx')
print ('Wrote Invoice_Sheet.xlsx')