import sys
# insert at 1, 0 is the script path (or '' in REPL)

import pytesseract
import cv2
import numpy as np
import os
from pytesseract import Output
from Spell_Checker.correction import spellCheck

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

def GenerateData (folder):
    dictList = []
    # for x in range(n)
    #     dictlist = [dict()]
    for file in os.listdir(folder):
        img = cv2.imread(folder+file)
        tempdict = pytesseract.image_to_data(img, output_type=Output.DICT) 
        newdict = {}
        texts = tempdict['text']
        tops = tempdict['top']
        lefts = tempdict['left']
        n = len(texts)
        for i in range(n):
            text = texts[i]
            if (text == ''):
                continue
            if (not hasCharacters(text)):
                newdict[text] = [tops[i], lefts[i]]
                continue
            if (hasNumbers(text) and len(text) < 2):
                newdict[text] = [tops[i], lefts[i]]
                continue
            text = text.upper()
            text = spellCheck(text)
            newdict[text] = [tops[i], lefts[i]]
        dictList.append(newdict)
            
    return dictList

# print(FindPONumber(lst))
# print(FindInvNumber(lst))
# print(spellCheck('GSTIN'))