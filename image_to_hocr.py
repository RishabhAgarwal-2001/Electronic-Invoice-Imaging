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

file_creative=r'test_inv_8.jpg'
image_creative = cv2.imread(file_creative, cv2.IMREAD_GRAYSCALE)
# image_creative=Image.open(file_creative)
hocr=pytesseract.image_to_data(image_creative, output_type=Output.DICT, config='--psm 4')
file=open("hocr_opt.html","w")
file.write(hocr)
file.close()
