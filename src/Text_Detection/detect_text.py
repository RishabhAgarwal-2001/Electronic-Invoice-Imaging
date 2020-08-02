try:
	from PIL import Image
except ImportError:
	import Image
import pytesseract
import os
import shutil

# Function to clean the directory storing the results
def clearTextFolder():
	crop_folder = '../results/crops_text/'
	for filename in os.listdir(crop_folder):
		file_path = os.path.join(crop_folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


def ocr_core(filename):
	text = pytesseract.image_to_string(Image.open(filename))
	return text

def convert_crops_to_text():

	clearTextFolder()

	print("Converting Crops to Text...")

	crop_folder = '../results/crops_localization/'
	text_folder = '../results/crops_text/'

	for filename in os.listdir(crop_folder):
		file_path = os.path.join(crop_folder, filename)
		text = ocr_core(file_path)
		name = text_folder + filename.split('.')[0] + ".txt"
		file = open(name, "w+")
		file.write(text)
		file.close()

	print("Conversion Completed... Results in results/crops_text !!!")