from Text_Localization.text_detect import text_detect
from Text_Localization.thresh import thresh
from Text_Localization.crop_images import createCrops
import cv2

class localTextRegion:
	"""docstring for localTextRegion"""
	def __init__(self, image):
		self.image = image
		self.image_copy = image.copy()
		print("Creating Mask...")
		self.mask, self.annotated_image = text_detect(self.image)
		print("Mask Created!!!\nIdentifying Regions....")
		self.dilated_mask, self.grouped_image, self.boundingBoxes = thresh(self.mask, self.image)
		print("Regions Identified!!!\nPreparing Crops...")
		createCrops(self.image_copy, self.boundingBoxes)
		print("Croping Completed!!!\n\nFind Results in Results\\crops_localization folder.")
		cv2.imshow('dilated Mask', self.dilated_mask)
		cv2.imshow('final', self.grouped_image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


# image = cv2.imread('/home/this/Flipkart_Challenge/GitHub Repo/Electronic-Invoice-Imaging/images/im9.png')
# obj = localTextRegion(image)
