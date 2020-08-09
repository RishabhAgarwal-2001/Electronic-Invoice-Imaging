from Text_Localization.text_detect import text_detect
from Text_Localization.thresh import thresh
from Text_Localization.crop_images import createCrops
import cv2
import os
import sys

class localTextRegion:
	counter = 1
	"""docstring for localTextRegion"""
	def __init__(self, image):
		c = 1
		crop_folder = "../results/crops_line/"
		for filename in os.listdir(crop_folder):
			# sys.stdout.write("\rProcessing: {}/{} Completed".format(c, len(os.listdir(crop_folder))))
			# sys.stdout.flush()
			file_path = os.path.join(crop_folder, filename)
			self.image = cv2.imread(file_path)
			self.image_copy = self.image.copy()
			# cv2.imshow("Before", self.image)
			self.image = cv2.copyMakeBorder(self.image, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
			# ret, self.image = cv2. threshold(self.image,127,255,cv2. THRESH_BINARY)
			self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
			clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
			self.image = clahe.apply(self.image)
			# cv2.imshow("Image", self.image)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			# cv2.imshow("Padded", self.image)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			self.mask, self.annotated_image = text_detect(self.image)
			# cv2.imshow("Mask", self.mask)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			self.dilated_mask, self.grouped_image, self.boundingBoxes = thresh(self.mask, self.image)
			self.counter = createCrops(self.image_copy, self.boundingBoxes, self.counter)
			c = c + 1
		# print()

		# self.image = image
		# self.image_copy = image.copy()
		# print("Creating Mask...")
		# self.mask, self.annotated_image = text_detect(self.image)
		# print("Mask Created!!!\nIdentifying Regions....")
		# self.dilated_mask, self.grouped_image, self.boundingBoxes = thresh(self.mask, self.image)
		# print("Regions Identified!!!\nPreparing Crops...")
		# createCrops(self.image_copy, self.boundingBoxes)
		# print("Croping Completed!!!\n\nFind Results in Results\\crops_localization folder.")
		# cv2.imshow('dilated Mask', self.dilated_mask)
		# cv2.imshow('final', self.grouped_image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()


# image = cv2.imread('/home/this/Flipkart_Challenge/GitHub Repo/Electronic-Invoice-Imaging/images/im9.png')
# obj = localTextRegion(image)
