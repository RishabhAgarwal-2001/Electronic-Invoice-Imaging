import numpy as np
import cv2
import os

def emptyFolder():
	crop_folder = '../results/table_meta_data'
	for filename in os.listdir(crop_folder):
		file_path = os.path.join(crop_folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


def cropTable(image, position):
	emptyFolder()
	metaData = image[:position+20, :]
	table = image[position-20:, :]
	crop_folder = '../results/table_meta_data/'
	metaDataFile = crop_folder + "metaData"+".png"
	tableFile = crop_folder + "table"+".png"
	cv2.imwrite(metaDataFile, metaData)
	cv2.imwrite(tableFile, table)