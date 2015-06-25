# ===================================

#  _     _     _     _     _ _     
# | |   (_)   | |   | |   (_) |    
# | |    _ ___| |_  | |    _| |__  
# | |   | / __| __| | |   | | '_ \ 
# | |___| \__ \ |_  | |___| | |_) |
# \_____/_|___/\__| \_____/_|_.__/ 

# ===================================

# Created by Gordon Estes

# Last Updated 6/1/15

# ===================================

import string

# ===================================

# Searches a list and all of its sublists for the given element.
def listContains(L,elem):
	#print("Checking list for element..."),
	for i in xrange(len(L)):
		try:
			if L[i] == elem:
				return True
		except:
			return False
		if str(type(L[i])) == "<type 'list'>" or str(type(L[i])) == "<type 'tuple'>":
			if listContains(L[i],elem): 
				return True
	#print("not found.")
	return False

# Takes in a list and a list containing all elements to be removed, and removes each 
# of those elements in turn from the list and any of its sublists/tuples.
def listRemove(L,rm_data):
	print("Removing elements from list...")
	del_list = []
	list_clean = []
	for i in xrange(len(L)):
		if str(type(L[i])) == "<type 'tuple'>":
			if L[i][0] in rm_data:
				del_list.append(i)
		else:
			if L[i] in rm_data:
				del_list.append(i)
	for i in xrange(len(L)):
		if i not in del_list:
			list_clean.append(L[i])
	return list_clean

def listRemoveTwo(L,rmData):
	print("Removing elements from list...")
	cleanList = []
	for i in xrange(len(L)):
		if str(type(L[i])) == "<type 'tuple'>" or str(type(L[i])) == "<type 'list'>":
			L[i] = listRemove(L[i],rmData)
		else:
			if L[i] not in rmData:
				cleanList.append(i)
	return cleanList

# Takes in a list of strings and replaces each substring of each 
# element/sublist of that list with the given string (def. "").
def replaceAll(L,s1,s2=""):
	for i in xrange(len(L)):
		if str(type(L[i])) == "<type 'str'>":
			string.replace(L[i],s1,s2)
		else:
			replaceAll(L[i],s1,s2)
	return L

# Takes in a (max 2-level) list and a level (def. 0) and converts that list
# to a printable string of format:
# [[1,2,3],[4,5,6],[7,8,9]]
# => 
# 1 | 2 | 3
# ----------
# 4 | 5 | 6
# ----------
# 7 | 8 | 9
# # NOTE: Incomplete/buggy.
# def listToString(L,level=0):
# 	result = ""
# 	addon = (" | ") if (level > 0) else ("-----------")
# 	for i in xrange(len(L)):
# 		if str(type(L[i])) == "<type 'str'>":
# 			result += (L[i] + addon)
# 		else:
# 			result += ("\n" + listToString(L[i],level+1))
# 			result += ("\n" + addon)
# 	return result

def getDepth(L):
	if str(type(L[0])) == "type 'list'>":
		return 1 + getDepth(L[0])
	else:
		return 1

def listToString(L):
	result = ""
	for elem in L:
		result += str(elem)
		result += "\n"
	return result

def mostlyIn(L1,L2):
	for sub in L1:
		if type(sub) != list: continue
		if len(sub) != len(L2): continue
		count = 0
		for i in xrange(len(L2)):
			if sub[i] == L2[i]: count += 1
		if count == len(L2) - 1: return True
	return False

def fromString(s):
	if s[0] != "[" or s[-1] != "]":
		return []
	return eval(s)

def toString(L):
	s = "["
	for i in xrange(len(L)):
		elem = L[i]
		if type(elem) == str:
			s += "\"%s\"" % elem
		elif type(elem) == list:
			s += toString(elem)
		else:
			s += str(elem)
		if i != len(L) - 1:
			s += ","
	s += "]"
	return s

