from Text_Localization.text_localization import localTextRegion
from Table_Start_Detection.detect_table import detectTable
from Table_Start_Detection.crop_table import cropTable
import cv2

fileName = 'im7_full.png'
tablePosition = detectTable(fileName)
image = cv2.imread('../images/'+fileName)
cropTable(image, tablePosition)
path_to_meta_data = '../results/table_meta_data/metaData.png'
path_to_table = '../results/table_meta_data/table.png'
metaData = cv2.imread(path_to_meta_data)
table = cv2.imread(path_to_table)
cv2.imshow("Meta Data", metaData)
cv2.imshow("Table", table)
cv2.waitKey(0)
cv2.destroyAllWindows()
# obj = localTextRegion(image)
