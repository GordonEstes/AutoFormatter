# -*- coding: utf-8 -*-

# ============================================
# ______           _____       _     _ _     
# | ___ \         |  ___|     | |   (_) |    
# | |_/ /___  __ _| |____  __ | |    _| |__  
# |    // _ \/ _` |  __\ \/ / | |   | | '_ \ 
# | |\ \  __/ (_| | |___>  <  | |___| | |_) |
# \_| \_\___|\__, \____/_/\_\ \_____/_|_.__/ 
#             __/ |                          
#            |___/                           

# ============================================

# Created by Gordon Estes

# Last Updated 6/1/15

# ============================================

import string
import os
import unicodedata
import re

# Removes all instances of a substring (sub) from a string (s). Possibly redundant.
# def removeAll(s,sub):
# 	while(match(s,sub) != -1):
# 		s = removeSub(s,sub)
# 	return s

# Returns a list containing the Unicode name of each sequential character in the
# given string (s).
def getChar(s):
	chars = ""
	for i in xrange(len(s)):
		chars += unicodedata.name(u'%s' % s[i])
		chars += "\n"
	return chars

# Takes in a string, a start index, and an end index, and returns a string with the 
# defined substring removed.
def removeIndices(text,start,end):
	if start >= len(text) or end < 0 or end <= start: 
		return text
	text = text[:start] + text[end:]
	return text

# Returns the number of instances of a regex substring within a larger string.
def findAll(s,sub):
	n = 0
	while True:
		i = match(s,sub)
		if i == -1: break
		s = s[i+len(sub):]
		n += 1
	return n

# Determines the equality of two strings using the match function.
def eq(s1,s2):
	if len(s1) != len(s2): return False
	if match(s1,s2) != 0: return False
	return True

# Determines whether two one-character strings are the same Unicode character.
def symbolEq(s1,s2):
	if len(s1) != len(s2): return False
	if len(s1) != 0: return False
	try:
		x1 = unicodedata.name(u'%s' % s1.decode('utf-8'))
		x2 = unicodedata.name(u'%s' % s2.decode('utf-8'))
	except:
		return False
	return x1 == x2

# Returns the starting index of the first instance of a regex substring within a 
# larger string, returning -1 if the substring is not present. Note that "@" stands
# for a wildcard, and "#" stands for an alphabetic wildcard (i.e., abc...ABC...).
def match(s,sub):
	if len(sub) > len(s): return -1
	if "@" not in sub and "#" not in sub and "<" not in sub and ">" not in sub:
		# return s.find(sub)
		try: return s.find(sub)
		except: pass
	i = 0 #Index within s
	k = 0 #Index within sub
	n = -1 #Beginning of sub within s
	found = False
	def success(i,k,n,found):
		if n == -1: n = i
		i += 1
		k += 1
		found = True
		return (i,k,n,found)
	while True:
		if k >= len(sub): return n #If we've reached the end of the substring, return n
		if i >= len(s): break
		if s[i] == sub[k]: (i,k,n,found) = success(i,k,n,found)
		elif sub[k] == "@": (i,k,n,found) = success(i,k,n,found)
		elif sub[k] == "#" and s[i] in string.ascii_letters: (i,k,n,found) = success(i,k,n,found)
		elif sub[k] == "<" and s[i] in string.ascii_lowercase: (i,k,n,found) = success(i,k,n,found)
		elif sub[k] == ">" and s[i] in string.ascii_uppercase: (i,k,n,found) = success(i,k,n,found)
		else: #Otherwise, if there's no match, start over.
			if found: i = n + 1
			else: i += 1
			found = False
			k = 0
			n = -1
	return -1

# Returns the word containing the character s[i] within string s.
# Returns " " if s[i] is blank and "" if i is out of range.
def getWord(s,i):
	if i >= len(s) or i < 0: return ""
	if s[i] == " ": return s[i]
	(j,k) = (i,i)
	while j > 0 and s[j] != " ": j -= 1
	while k < len(s) and s[k] != " ": k += 1
	return s[j+1:k]

# Returns the word previous to the word containing the character s[i]
# within string s.
def prevWord(s,i):
	if i <= 0 or i >= len(s): return None
	if s[i] == " ": return prevWord(s,i-1)
	j = i
	while j >= 0 and s[j] != " ": j -= 1
	return getWord(s,j-1)

# Returns the word following the word containing the character s[i]
# within string s.
def nextWord(s,i):
	if i >= len(s) - 1: return None
	if s[i] == " ": return nextWord(s,i+1)
	k = i
	while k <= len(s) - 1 and s[k] != " ": k += 1
	return getWord(s,k+1)

# Returns a version of string s with the first instance of the word containing 
# the character s[i] replaced with the substring (new)
def replaceThisWord(s,i,new):
	if i >= len(s) or i < 0: return s
	if s[i] == " ": return s
	j = i
	k = i
	while j > 0 and s[j] != " ": j -= 1
	while k < len(s) and s[k] not in " .,:;'-!?": k += 1
	s = s[:j+1] + new + s[k:]
	return s

# Returns the index (i) of the full word corresponding to the substring(sub)
# within string (s).
def matchWord(s,sub,n=0):
	i = match(s,sub)
	if i == -1: return -1
	if i > 0 and (i + len(sub) < len(s) - 1):
		if s[i-1] == " " and s[i+len(sub)] in u'.,;:"-—!? ': return i+n
		if s[i-1] in u"—\"" and s[i+len(sub)] == " ": return i+n
	elif i == 0 and (i + len(sub) < len(s) - 1):
		if s[i+len(sub)] in u'.,;:"-—!? ': return i+n
	elif i > 0 and (i + len(sub) == len(s)):
		if s[i-1] == " ": return i+n
	s = s[i+len(sub):]
	return matchWord(s,sub,n+i+len(sub))

# Removes a regex substring from a larger string and returns the result.
def removeSub(s,sub):
	return replaceSub(s,sub,"")
	# i = 0
	# while True:
	# 	i = match(s,sub)
	# 	if i == -1: 
	# 		break
	# 	s = s[:i] + s[i+len(sub):]
	# return s

# Returns a version of string (s) with the character at index (i) replaced
# with the character (t).
def replaceIndex(s,i,t):
	if i < 0 or i >= len(s): return s
	return s[:i] + t + s[i+1:]

# Returns a version of the string (s) with all instances of substring (sub)
# replaced with the substring (new).
def replaceSub(s,sub,new):
	while True:
		i = match(s,sub)
		newer = new
		if i == -1: 
			break
		if len(new) == len(sub) and "@" in new or "#" in new:
			for j in xrange(len(new)):
				if new[j] in "@#":
					newer = replaceIndex(newer,j,s[i+j])
		s = "%s%s%s" % (s[:i],newer,s[i+len(sub):])
	return s

# Returns a version of the string (s) with all full-word instances of the
# substring (sub) replaced with the substring (new).
def replaceWord(s,sub,new):
	while True:
		i = matchWord(s,sub)
		if i == -1: 
			break
		s = "%s%s%s" % (s[:i],new,s[i+len(sub):])
	return s

# Returns the index of the first non-integer character in the given string.
def nextNonInt(s):
	for i in xrange(len(s)):
		if s[i] not in "1234567890":
			return i 
	return -1 

# Returns the index of the first integer character in the given string.
def nextInt(s):
	for i in xrange(len(s)):
		if s[i] in "1234567890":
			return i
	return -1

# Useless. Disregard this :V
def toFront(s,sub):
	i = match(s,sub)
	if i == -1: 
		return s
	k = i + len(sub)
	s = removeIndices(s,i,k)
	if len(s) >= 2 and s[0:2] == ", ": 
		s = s[2:]
	s = sub + s
	return s

# Checks whether a given string is comprised entirely of integers.
def isInt(s):
	if s == "":
		return False
	for c in s:
		if c not in "1234567890": 
			return False
	return True

# Returns the type of value x in string form.
def stype(x):
	return str(type(x))

# Returns a reversed form of string x.
def reverse(x):
	return x[::-1]

# Returns a copy of string (s) with the ending clipped up to and including
# substring (x) (e.g. clipRight('hello.doc','doc') => 'hello').
def clipRight(s,x):
	s = reverse(s)
	i = match(s,x)
	k = i + len(x)
	s = s[k:]
	return reverse(s)

def getRange(s):
	j = s.find("[")
	k = s.find("]")
	s = s[j+1:k]
	if len(s) == 3 and s[1] == "-" and s[0] != "\\":
		if s[0] in string.ascii_lowercase and s[2] in string.ascii_lowercase:
			i = string.ascii_lowercase.find(s[0])
			j = string.ascii_lowercase.find(s[2])
			if j < i: return ""
			return string.ascii_lowercase[i:j+1]
		elif s[0] in string.ascii_uppercase and s[2] in string.ascii_uppercase:
			i = string.ascii_uppercase.find(s[0])
			j = string.ascii_uppercase.find(s[2])
			if j < i: return ""
			return string.ascii_uppercase[i:j+1]
	else:
		charRange = ""
		i = 0
		while i < len(s):
			if s[i] == "\\" and i < len(s) - 1:
				charRange = charRange + s[i+1]
				i += 2
			else:
				charRange = charRange + (s[i])
				i += 1
		return charRange

def rxSplit(s):
	subList = []
	j = s.find("[")
	k = s.find("]")
	done = False
	while True:
		if j == -1 or k == -1 or k < j: break
		charRange = getRange(s)
		sub = s[:j] + "@"
		s = s[k+1:]
		subList.append((sub,charRange))
		j = s.find("[")
		k = s.find("]")
	if s != "": subList.append((s,""))
	return subList

def rxFind(s,sub):
	subList = rxSplit(sub)
	i = 0 #Index within s
	j = 0 #Index within sublist
	k = 0 #Index within sub
	n = -1 #Beginning of sub within s
	found = False
	def success(i,j,k,n,found):
		if n == -1: n = i
		i += 1
		k += 1
		if k >= len(sub):
			j += 1
			k = 0
		found = True
		return (i,j,k,n,found)
	while True:
		if j >= len(subList): return n #If we've reached the end of the substring, return n
		(sub,charRange) = subList[j]
		if i >= len(s): break
		if s[i] == sub[k]: (i,j,k,n,found) = success(i,j,k,n,found)
		elif sub[k] == "@" and s[i] in charRange: (i,j,k,n,found) = success(i,j,k,n,found)
		else: #Otherwise, if there's no match, start over.
			if found: i = n + 1
			else: i += 1
			found = False
			k = 0
			n = -1
	return -1

def endsWith(s,sub):
	l = len(sub)
	s = s[-l:]
	return (rxFind(s,sub) != -1)

def rxReplace(s,sub,new):
	while True:
		i = rxFind(s,sub)
		newer = new
		if i == -1: 
			break
		if len(new) == len(sub):
			for j in xrange(len(new)):
				if new[j] in "@#":
					newer = replaceIndex(newer,j,s[i+j])
		s = "%s%s%s" % (s[:i],newer,s[i+len(sub):])
	return s

s = re.compile('hello world')
s2 = 'llo w'
print s.search(s2)