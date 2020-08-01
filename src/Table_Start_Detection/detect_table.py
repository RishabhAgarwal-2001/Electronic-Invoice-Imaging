import pytesseract
from pytesseract import Output
import cv2
import numpy as np


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def myround(x, base=25):
    return base * round(x/base)


def detectTable(fileName):
	header_keyWords = ['MATERIAL', 'DESCRIPTION', 'HSN', 'QTY', 'QUANTITY', 'UNIT PRICE', 'TOTAL', 'DISCOUNT', 'TAXABLE VALUE',
	'AMOUNT', 'IGST', 'AMT', 'S. NO.', 'RATE', 'CGST', 'SGST', 'UGST', 'ITEM', 'CODE', 'CATEGORY', 'SIZE', 'PC', 'PCS', 'PIECES',
	'MRP', 'DISC.', 'BASIC', 'SELLING', 'PRICE', 'VALUE', 'INVOICE', 'GST', 'GOODS', 'PER', 'SERIAL', 'NUMBER', 'NO', 'TAX', 'TAXABLE',
	'MEASUREMENT', 'SAC', 'BATCH', 'MFG.', 'AMT', 'PRODUCT', 'CESS', 'UOM', 'GROSS', 'TAX', 'SERVICE', 'DISC', 'NOS', 'NOS.']

	img = cv2.imread('/home/this/Flipkart_Challenge/GitHub Repo/Electronic-Invoice-Imaging/images/'+fileName)

	d = pytesseract.image_to_data(img, output_type=Output.DICT)

	text = d['text']
	top = d['top']

	tx = []
	pos = []

	for i in range(len(text)):
		currentText = text[i].upper()
		currrenTop = top[i]
		flag = False
		for words in header_keyWords:
			if(levenshteinDistance(currentText, words)<2):
				flag = True
				break
		if(flag==True):
			tx.append(currentText)
			pos.append(currrenTop)

	pos_copy = pos[:]

	for i in range(len(pos)):
		pos[i] = myround(pos[i])


	position = max(pos,key=pos.count)

	linePos = 1000000
	for i in range(len(pos)):
		if(pos[i]==position):
			linePos = min(linePos, pos_copy[i])

	position = linePos - 15

	return position