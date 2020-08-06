'''
Key Values that I am looking for-
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Phase 1																	|
====================================									|
From: Address, Name, State, Telephone, PAN, GSTNo						|
====================================									|
To: Address, Name, State, Telephone, PAN, GSTNo							|
====================================									|
Bill To: Address, Name, State, Telephone, PAN, GSTNo					|
====================================									|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
import re
import math

def findValues(dictionaryList):
	'''
	Input Parameter: A List of Dictionary, where each dictionary has keys as corrected words
	and values as a list of top and left position in that specific crop
	'''
	buyerData = findBuyerValues(dictionaryList)

def matchesGST(txt):
	gstRegEx = "\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"
	x = re.search(gstRegEx, txt)
	if(x):
		return True
	else:
		return False

def distance(point1, point2, choice=1):
	if(choice==1):
		return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])
	else:
		x = abs(point1[0]-point2[0])
		y = abs(point1[1]-point2[1])
		return math.sqrt(x*x+y*y)


# Buyer, Customer, Ship to, Billed to, Consignee, Shipped
def findBuyerValues(dictionaryList):
	keyWords = ["BUYER", "BUY", "BOUGHT", "CUSTOMER", "CONSIGNEE", "SHIPPED", "BILLED"]
	results = {}
	for currentDictionary in dictionaryList:

		# List containing all Words in the given crop
		words = currentDictionary.keys()

		# Checking if the crop contains information about the Buyer
		valid = False
		for w in words:
			if(w.upper() in keyWords):
				valid = True
				break
		if(valid==False):
			continue
		
		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		GST_Value = "" # Variable to Store the value of GST Number
		GST_Value_loc = math.inf # Variable to store the location of GST Number
		GST_Location = None # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			if(re.search("^GST", w)):
				GST_Location = currentDictionary[w]
				break
		# If Key GST exists
		if(GST_Location is not None):
			print(GST_Location)
			for w in words:
				if(matchesGST(w) and distance(currentDictionary[w], GST_Location, 2)<GST_Value_loc):
					GST_Value = w
					GST_Value_loc = distance(currentDictionary[w], GST_Location, 2)
					print("Distance = ", GST_Value_loc)
		results["GST"] = [GST_Value, GST_Value_loc]
		# ---------------------------------------------------------------

	return results

print(findBuyerValues([{"BOUGHT":[10, 10], "18AABCU9603R1ZM":[20, 20], "18AABCU9603R1ZQ":[50, 50], "GSTIN":[12, 50]}]))
