# ===================================

# ______ _ _        _     _ _     
# |  ___(_) |      | |   (_) |    
# | |_   _| | ___  | |    _| |__  
# |  _| | | |/ _ \ | |   | | '_ \ 
# | |   | | |  __/ | |___| | |_) |
# \_|   |_|_|\___| \_____/_|_.__/                     
                                
# ===================================

# Created by Gordon Estes

# Last Updated 6/1/15

# ===================================

import os
import string

# Reads from a given .txt file and returns the contents as a string.
# Copied from: https://www.cs.cmu.edu/~112/notes/file-and-web-io.py
def readFile(filename,mode="rt"):
	fin = contents = None
	try:
		fin = open(filename, mode)
		contents = fin.read()
	finally:
		if (fin != None): fin.close()
	return contents

# Writes a string to a .txt file.
# Coped from: https://www.cs.cmu.edu/~112/notes/file-and-web-io.py
def writeFile(filename,contents,mode="wt"):
	with open(filename, mode) as fout:
		fout.write(contents)

def appendFile(filename,contents):
	text = readFile(filename)
	if text != "": text += "\n"
	text = text + contents
	writeFile(filename,text)