from Text_Localization.text_localization import localTextRegion
import cv2

fileName = 'im6.png'
image = cv2.imread('/home/this/Flipkart_Challenge/GitHub Repo/Electronic-Invoice-Imaging/images/'+fileName)
obj = localTextRegion(image)