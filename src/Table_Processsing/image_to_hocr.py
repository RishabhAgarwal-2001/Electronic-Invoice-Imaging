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
from pytesseract import Output


def image_2_hocr():
    file_creative='../results/test_inv_8.jpg'
    image_creative = cv2.imread(file_creative, cv2.IMREAD_GRAYSCALE)
    # image_creative=Image.open(file_creative)
    hocr = str(pytesseract.image_to_pdf_or_hocr(file_creative, extension='hocr'))
    # hocr=pytesseract.image_to_data(image_creative, output_type=Output.DICT, config='--psm 4')
    hocr = hocr.replace('\\n', '\n')
    file=open("../results/hocr_opt.html","w")
    file.write(hocr)
    file.close()

