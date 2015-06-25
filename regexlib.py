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

def removeAll(s,sub):
	while(match(s,sub) != -1):
		s = removeSub(s,sub)
	return s

def replaceAll(s,sub,new):
	while(match(s,sub) != -1):
		s = replaceSub(s,sub,new)
	return s

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

def eq(s1,s2):
	if len(s1) != len(s2): return False
	if match(s1,s2) != 0: return False
	return True

def symbolEq(s1,s2):
	try:
		x1 = unicodedata.name(u'%s' % s1.decode('utf-8'))
		x2 = unicodedata.name(u'%s' % s2.decode('utf-8'))
	except:
		return False
	return x1 == x2

# Returns the starting index of the first instance of a regex substring within a 
# larger string, returning -1 if the substring is not present.
def match(s,sub):
	if len(sub) > len(s): return -1
	i = 0 #Index within s
	k = 0 #Index within sub
	n = -1 #Beginning of sub within s
	found = False
	while True:
		if k >= len(sub): return n #If we've reached the end of the substring, return n
		if i >= len(s): break
		if s[i] == sub[k]: #If they match, advance both.
			if n == -1: n = i
			i += 1
			k += 1
			found = True
		elif sub[k] == "@": #If it's a wildcard, same thing.
			if n == -1: n = i
			i += 1
			k += 1
			found = True
		elif sub[k] == "#" and s[i] in string.ascii_letters:
			if n == -1: n = i
			i += 1
			k += 1
			found = True
		else: #Otherwise, if there's no match, start over.
			if found: i = n + 1
			else: i += 1
			found = False
			k = 0
			n = -1
	return -1

def getWord(s,i):
	if s[i] == " ": return s[i]
	(j,k) = (i,i)
	while j > 0 and s[j] != " ": j -= 1
	while k < len(s) and s[k] != " ": k += 1
	return s[j+1:k]

def prevWord(s,i):
	if i <= 0: return None
	if s[i] == " ": return prevWord(s,i-1)
	j = i
	while j >= 0 and s[j] != " ": j -= 1
	return getWord(s,j-1)

def nextWord(s,i):
	if i >= len(s) - 1: return None
	if s[i] == " ": return nextWord(s,i+1)
	k = i
	while k <= len(s) - 1 and s[k] != " ": k += 1
	return getWord(s,k+1)

def replaceThisWord(s,i,new):
	if i >= len(s) or i < 0: return s
	if s[i] == " ": return s
	j = i
	k = i
	while j > 0 and s[j] != " ": j -= 1
	while k < len(s) and s[k] not in " .,:;'-!?": k += 1
	s = s[:j+1] + new + s[k:]
	return s

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
	i = 0
	while True:
		i = match(s,sub)
		if i == -1: 
			break
		s = s[:i] + s[i+len(sub):]
	return s

def replaceIndex(s,i,t):
	if i < 0 or i >= len(s): return s
	return s[:i] + t + s[i+1:]

def replaceSub(s,sub,new):
	while True:
		i = match(s,sub)
		newer = new
		if i == -1: 
			break
		if len(new) == len(sub):
			for j in xrange(len(new)):
				if new[j] in "@#":
					newer = replaceIndex(newer,j,s[i+j])
		s = "%s%s%s" % (s[:i],newer,s[i+len(sub):])
	return s

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

def nextInt(s):
	for i in xrange(len(s)):
		if s[i] in "1234567890":
			return i
	return -1

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

def isInt(s):
	if s == "":
		return False
	for c in s:
		if c not in "1234567890": 
			return False
	return True

def stype(x):
	return str(type(x))

def reverse(x):
	return x[::-1]

def clipRight(s,x):
	s = reverse(s)
	i = match(s,x)
	k = i + len(x)
	s = s[k:]
	return reverse(s)
