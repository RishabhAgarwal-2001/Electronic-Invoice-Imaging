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
	# for i in dictionaryList:
	# 	# print(i)
	# # print()
	results = {}
	buyerData = findBuyerValues(dictionaryList)
	billToData = findBillerValue(dictionaryList)
	results = {**buyerData, **billToData}
	return results

def matchesGST(txt):
	gstRegEx = "\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{2}[Z]{1}[A-Z\d]{1}"
	x = re.search(gstRegEx, txt)
	if(x):
		return True
	else:
		return False

def matchesPO(txt):
	poRegEx = "^PO\d{7}$"
	x = re.search(poRegEx, txt)
	if(x):
		return True
	else:
		poRegEx = "^\d{7}$"
		x = re.search(poRegEx, txt)
		if(x):
			return True
		else:
			return False

def matchesInvNo(txt):
	invRegEx = "^\d{4}$"
	x = re.search(invRegEx, txt)
	if(x):
		return True
	else:
		return False

def matchesDate(txt):
	invRegEx = "^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(/|-|.)(0[1-9]|[1-9]|1[0-2])(/|-|.)(20[0-9][0-9])$"
	x = re.search(invRegEx, txt)
	if(x):
		return True
	else:
		return False

def matchesPAN(txt):
	panRegEx = "^([A-Z]{5}[0-9]{4}[A-Z]{1})"
	x = re.search(panRegEx, txt)
	if(x):
		return True
	else:
		return False

def distance(point1, point2, choice=1):
	# # print(point1, point2)
	if(choice==1):
		return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])
	elif(choice==2):
		x = abs(point1[0]-point2[0])
		y = abs(point1[1]-point2[1])
		return math.sqrt((x*x)+(y*y))
	elif(choice==3):
		x = abs(point1[0]-point2[0])
		y = abs(point1[1]-point2[1])
		return min(x, y)


# Assuming values in form (left, top)
def wordsNext(dictionary, location, neighbourCount=1):

	pairs = []
	for k in dictionary.keys():
		pairs.append([k, dictionary[k]])

	pairs = sorted(pairs, key = lambda x: (x[1][0], x[1][1]))

	alpha = location[:]

	
	neigh = []
	
	for i in pairs:
		if(isGreater(alpha, i[1])):
			neigh.append(i[0])

	return neigh[:neighbourCount]

def isGreater(point1, point2):
	if(point1[0]-22<point2[0] and point1[1]-22<point2[1]):
		return True
	else:
		return False

def isBelow (point1, point2):
	if (point1[0] - 5 < point2[0]):
		return True
	else:
		return False


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def checkState(word):
	states = ["Andhra", "Arunachal", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal", "Jammu", "Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
           "Punjab", "Rajasthan", "Sikkim", "Tamil", "Nadu", "Telangana", "Tripura", "Uttar", "Uttarakhand", "West", "Bengal", "Andaman", "Nicobar", "Chandigarh", "Dadra", "Nagar", "Haveli", "Daman", "Diu", "Lakshadweep", "Delhi", "Puducherry"]
	for s in states:
		s = str(s.upper())
		if(levenshteinDistance(s, word)<2 or re.search(s, word.upper())):
			return s.upper()
	return ""

def NoOfDigits(inputString):
	count = 0
	for char in inputString:
		if (char.isdigit()):
			count += 1
	return count

def findBillerValue(dictionaryList):
	keyWords = ["BILL-TO", "BUYER", "BILLING"]
	keyWords_to = ["BILL", "BILLED", "SOLD"]
	results = {"BILLED_GST": "", "BILLED_PAN": "", "BILLED_STATE": ""}
	for currentDictionary in dictionaryList:
		# List containing all Words in the given crop
		words = currentDictionary.keys()

		loc = [-1, -1]

		# Checking if the crop contains information about the Buyer
		valid = False
		for w in words:
			if(w.upper() in keyWords):
				valid = True
				loc = currentDictionary[w]
				break
			if(w.upper() in keyWords_to):
				# print("Found Something Here ", w.upper())
				neigh = wordsNext(currentDictionary, currentDictionary[w], 10)
				# print(neigh)
				for i in neigh:
					if(re.search("TO", i)):
						# print("Found TO")
						valid = True
						loc = currentDictionary[w]
						break
			

		if(valid == False):
			continue

		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		GST_Value = ""  # Variable to Store the value of GST Number
		GST_Location = None  # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			if((re.search("^TIN", w) or re.search("^GST", w) or re.search("^STI", w)) and isBelow(loc, currentDictionary[w])):
				GST_Location = currentDictionary[w]
				# print("FOUnd GST at ", GST_Location)
				break
		# If Key GST exists
		if(GST_Location is not None):
			neigh = wordsNext(currentDictionary, GST_Location, 25)
			# print(neigh)
			for i in neigh:
				if(len(i) > 12 or matchesGST(i)):
					GST_Value = i
					break
			results["BILLED_GST"] = GST_Value
		else:
			neigh = wordsNext(currentDictionary, loc, 25)
			for i in neigh:
				if(len(i)>12 or matchesGST(i)):
					GST_Value = i
					break
			results["BILLED_GST"] = GST_Value
		# ---------------------------------------------------------------

		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		PAN_Value = ""  # Variable to Store the value of GST Number
		PAN_Location = None  # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			if(re.search("^PAN", w) and isBelow(loc, currentDictionary[w])):
				PAN_Location = currentDictionary[w]
				break
		# If Key GST exists
		if(PAN_Location is not None):
			neigh = wordsNext(currentDictionary, PAN_Location, 20)
			for i in neigh:
				if((len(i) > 8 and len(i)<10 and NoOfDigits(i) > 2 and NoOfDigits(i) < 7) or matchesPAN(i)):
					PAN_Value = i
					break
			results["BILLED_PAN"] = PAN_Value
		# ---------------------------------------------------------------

		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		STATE_Value = ""  # Variable to Store the value of GST Number
		STATE_Location = None  # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			if(re.search("STATE", w) and isBelow(loc, currentDictionary[w])):
				STATE_Location = currentDictionary[w]
				break
			if(re.search("PLACE", w)):
				neigh = wordsNext(currentDictionary, currentDictionary[w], 20)
				for x in neigh:
					if(re.search("SUPPLY", x.upper()) or re.search("DELIVER", x.upper())):
						STATE_Location = currentDictionary[w]
						break
				if(STATE_Location is not None):
					break
		# If Key GST exists
			if(STATE_Location is not None):
				neigh = wordsNext(currentDictionary, STATE_Location, 20)
				for i in neigh:
					if(checkState(i)!=''):
						STATE_Value = checkState(i)
						break
			results["BILLED_STATE"] = STATE_Value
		# ---------------------------------------------------------------



	return results

# Buyer, Customer, Ship to, Billed to, Consignee, Shipped
def findBuyerValues(dictionaryList):
	keyWords = ["CUSTOMER", "CONSIGNEE", "SHIPPING", "SHIP-TO", "SUPPLY", "SHIP-TO:"]
	keyWords_to = ["SHIPPED", "SHIP"]
	keyWords_by = ["BOUGHT"]
	
	results = {"SHIPPED_GST": "", "SHIPPED_PAN": "", "SHIPPED_STATE": ""}
	for currentDictionary in dictionaryList:
		# List containing all Words in the given crop
		words = currentDictionary.keys()

		loc = [-1, -1]

		# Checking if the crop contains information about the Buyer
		valid = False
		for w in words:
			for x in keyWords:
				if (re.search(x, w)):
					valid = True
					loc = currentDictionary[w]
					break
			if(w.upper() in keyWords):
				valid = True
				loc = currentDictionary[w]
				break
			if(w.upper() in keyWords_to):
				neigh = wordsNext(currentDictionary, currentDictionary[w], 5)
				for i in neigh:
					if(re.search("TO", i)):
						valid = True
						loc = currentDictionary[w]
						break
			if(w.upper() in keyWords_by):
				neigh = wordsNext(currentDictionary, currentDictionary[w], 5)
				for i in neigh:
					if(re.search("BY", i)):
						valid = True
						loc = currentDictionary[w]
						break

		if(valid==False):
			continue
		
		# # print("Customer Crop:", loc)
		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		GST_Value = "" # Variable to Store the value of GST Number
		GST_Location = None # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			# # print("W: ",w, currentDictionary[w])
			if((re.search("^TIN", w) or re.search("^GST", w) or re.search("^STI", w)) and isBelow(loc, currentDictionary[w])):
				GST_Location = currentDictionary[w]
				# # print("Found GST At Location: ", GST_Location)
				break
		# If Key GST exists
		if(GST_Location is not None):
			neigh = wordsNext(currentDictionary, GST_Location, 25)
			# # print(neigh)
			for i in neigh:
				if(len(i)>12 or matchesGST(i)):
					GST_Value = i
					break
			results["SHIPPED_GST"] = GST_Value
		else:
			neigh = wordsNext(currentDictionary, loc, 25)
			for i in neigh:
				if(len(i)>12 or matchesGST(i)):
					GST_Value = i
					break
			results["SHIPPED_GST"] = GST_Value
		# ---------------------------------------------------------------


		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		PAN_Value = "" # Variable to Store the value of GST Number
		PAN_Location = None # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			if(re.search("^PAN", w) and isBelow(loc, currentDictionary[w])):
				PAN_Location = currentDictionary[w]
				break
		# If Key GST exists
		if(PAN_Location is not None):
			neigh = wordsNext(currentDictionary, PAN_Location, 20)
			for i in neigh:
				if((len(i)>8 and len(i)<10 and NoOfDigits(i) > 2 and NoOfDigits(i) < 7) or matchesPAN(i)):
					PAN_Value = i
					break
			results["SHIPPED_PAN"] = PAN_Value
		# ---------------------------------------------------------------

		# ---------------------------------------------------------------
		# Finding GST Number in the array of words
		STATE_Value = ""  # Variable to Store the value of GST Number
		STATE_Location = None  # Variable to Store the Location of KEY GST
		# Looking for Key GST in words
		for w in words:
			if(re.search("STATE", w) and isBelow(loc, currentDictionary[w])):
				STATE_Location = currentDictionary[w]
				break
			if(re.search("PLACE", w)):
				neigh = wordsNext(currentDictionary, currentDictionary[w], 20)
				for x in neigh:
					if(re.search("SUPPLY", x.upper()) or re.search("DELIVER", x.upper())):
						STATE_Location = currentDictionary[w]
						break
				if(STATE_Location is not None):
					break
		# If Key GST exists
		if(STATE_Location is not None):
			# # print("State Found--------")
			neigh = wordsNext(currentDictionary, STATE_Location, 20)
			# # print(neigh)
			for i in neigh:
				if(checkState(i) != ''):
					STATE_Value = checkState(i)
					break
		results["SHIPPED_STATE"] = STATE_Value
		# ---------------------------------------------------------------

	return results

def FindPONumber(lod):
	dictionary = {}
	for currdict in lod:
		for text in currdict.keys():
			if (matchesPO(text)):
				dictionary['PO NUMBER'] = text
				if (text[:2] == "PO"):
					return dictionary
				else:
					listOfWords = wordsNext(currdict, currdict[text], 3)
					for i in listOfWords:
    						if (i == 'PO' or i == 'PURCHASE' or i == 'SUPPLIER' or i == 'BUYER'):
    								return dictionary
	return dictionary

def FindInvNumber(lod):
	dictionary = {}
	for currdict in lod:
		for text in currdict.keys():
			if (text == 'INVOICE'):
				minDis = math.inf	
				for text2 in currdict.keys():			
					if (matchesInvNo(text2) and minDis > distance(currdict[text2], currdict[text], 2)):
						dictionary['INVOICE NUMBER'] = text2
						minDis = distance(currdict[text2], currdict[text], 2)
				if (minDis < math.inf):
					return dictionary
				continue
	return dictionary

def FindDate(lod, dateList):
	dictionary = {}
	for currdict in lod:
		for text in currdict.keys():
			for dateFormat in dateList:
				if (text == dateFormat):
					# # print(text)
					# # print(currdict[text])
					neighbours = wordsNext (currdict, currdict[text], 10)
					# if (text == 'INVOICE'):
					# 	# print(neighbours)
					# # print(neighbours)
					date = ''
					for i in neighbours:
						if (matchesDate(i)):
							date = i
					if (date != ''):
						if (text == 'DATED' or text == 'DATE'):
							dictionary[text] = date
						else:
							dictionary[text+' DATE'] = date
	return dictionary

def FindCurrency(lod):
	dictionary = {}
	for currdict in lod:
		for text in currdict.keys():
			if (text == 'CURRENCY'):
				# # print(text)
				# # print(currdict[text])
				neighbours = wordsNext (currdict, currdict[text], 10)
				# # print(neighbours)
				for i in neighbours:
					if (i == 'USD' or i == 'INR'):
						dictionary[text] = i
						return dictionary
	return dictionary

# # print(findBuyerValues([{"BOUGHT":[10, 10], "18AABCU9603R1ZM":[20, 20], "18AABCU9603R1ZQ":[50, 50], "GSTIN":[12, 50],
	# "PAN":[20, 20], "BNZAA2318J":[20, 25]}]))

# # print (matchesGST('07AABBC8888G1AZ1'))
# # print(matchesDate('01.07.2017'))