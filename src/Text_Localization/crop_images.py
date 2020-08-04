import cv2
import os, shutil


def emptyFolder():
	crop_folder = '../results/crops_localization'
	for filename in os.listdir(crop_folder):
		file_path = os.path.join(crop_folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

def createCrops(image, boundingBoxes, counter):
	if(counter==1):
		emptyFolder()
	crop_folder = '../results/crops_localization/'
	for bbox in boundingBoxes:
		x, y, w, h = bbox
		crop = image[y:y+h, x:x+w]
		cropName = crop_folder + "Crop_" + str(counter) + ".jpg"
		counter = counter + 1 
		cv2.imwrite(cropName, crop)
	return counter