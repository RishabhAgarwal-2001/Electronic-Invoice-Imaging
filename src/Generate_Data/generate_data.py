import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../Spell_Checker')

import pytesseract
import cv2
import numpy as np
import os
from pytesseract import Output
from . import spellCheck

def hasNumbers(inputString):
    for char in inputString:
        if (char.isdigit()):
            return True
    return False

def hasCharacters(inputString):
    for char in inputString:
        if (char.isalpha()):
            return True
    return False

def GenerateData ():
    folder = '../../results/crops_localization/'
    dictList = []
    # for x in range(n)
    #     dictlist = [dict()]
    for file in os.listdir(folder):
        img = cv2.imread(folder+file)
        dictList.append(pytesseract.image_to_data(img, output_type=Output.DICT))  
    for i in dictList:
        texts = i['text']
        for text in texts:
            if (hasNumbers(text) or not hasCharacters(text)):
                continue
            print(text)

GenerateData()