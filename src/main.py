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
from pdf2image import convert_from_path
import time
from yaspin import yaspin
from Table_Processsing.image_cut_and_rejoin import cut_rejoin
from Table_Processsing.image_to_hocr import image_2_hocr
from Table_Processsing.hocr_to_table import hocr2table
import argparse



with yaspin(text=" ", color="yellow").bouncingBar as spinner:

	parser = argparse.ArgumentParser()

	parser.add_argument("-i", "--input", required=True, help="path to input pdf")
	parser.add_argument("-o", "--output", required=True,
						help="path to output spreadSheet")
	args = vars(parser.parse_args())

	pdf_path = args["input"]
	output_path = args["output"]

	images = convert_from_path(pdf_path)
	images[0].save("../images/input.png")

	fileName = "input.png"

	# Deskewing Image
	image = cv2.imread('../images/input.png')
	deskewImage(image)


	# Detecting and Separating MetaData and Table out of the invoice Image
	# print("Table and Meta Data Separation Started...")
	tablePosition = detectTable(fileName)
	image = cv2.imread('../results/deskew_image/image.png')
	cropTable(image, tablePosition)
	# spinner.hide()
	# print("Table and Meta Data Separation Completed!!!\n")
	# spinner.show()


	# Reading in the metaData and Table Image
	path_to_meta_data = '../results/table_meta_data/metaData.png'
	path_to_table = '../results/table_meta_data/table.png'
	metaData = cv2.imread(path_to_meta_data)
	table = cv2.imread(path_to_table)

	# Cropping Based on Lines
	# print("Cropping Meta Data Image Based on Horizontal And Vertical Lines...")
	EdgeDetectionAll(path_to_meta_data, False)
	

	# Separating Meta Data Regions
	obj = localTextRegion(metaData)

	# Converting Crops into text
	convert_crops_to_text()

	spinner.hide()
	print("Preprocessing Completed!!!")
	spinner.show()

	folder = '../results/crops_localization/'
	print("Generating Data...")
	lst = GenerateData(folder)
	folder = '../results/crops_line/'
	lst2 = GenerateData(folder)
	# print(lst)
	print("Finding Values...")
	finalDict1 = findValues(lst)
	finalDict1.update(FindPONumber(lst))
	finalDict1.update(FindInvNumber(lst))
	dateList = ['LR', 'INVOICE', 'DA', 'DELIVERY', 'PURCHASE', 'PO', 'DUE', 'LOA', 'ORDER', 'PICKING', 'PASS', 'CHALLAN', 'DISPATCH', 'SO', 'DATED', 'REF']
	finalDict1.update(FindDate(lst, dateList))
	finalDict1.update(FindCurrency(lst))

	finalDict2 = findValues(lst2)
	finalDict2.update(FindPONumber(lst2))
	finalDict2.update(FindInvNumber(lst2))
	finalDict2.update(FindDate(lst2, dateList))
	finalDict2.update(FindCurrency(lst2))

	finalDict = {**finalDict1, **finalDict2} 
	# print("Final Dictionary: ",finalDict)

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
	spinner.hide()
	print ('Wrote Invoice_Sheet.xlsx')
	spinner.show()
	cut_rejoin()
	image_2_hocr()
	hocr2table()

	# Add Ouput Path to Excel Sheet
	# wb.save(output_path + "/Invoice_Sheet.xls")

	spinner.ok("✅ EXCEL SHEET GENERATED")
