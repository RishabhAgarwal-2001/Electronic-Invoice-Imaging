from Text_Localization.text_detect import text_detect
from Text_Localization.thresh import thresh
import cv2

class localTextRegion:
	"""docstring for localTextRegion"""
	def __init__(self, image):
		self.image = image
		self.mask, self.annotated_image = text_detect(self.image)
		self.dilated_mask, self.grouped_image, self.boundingBoxes = thresh(self.mask, self.image)
		cv2.imshow('final', self.grouped_image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


# image = cv2.imread('/home/this/Flipkart_Challenge/GitHub Repo/Electronic-Invoice-Imaging/images/im9.png')
# obj = localTextRegion(image)