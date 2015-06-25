# -*- coding: utf-8 -*-

# ===========================================================================

#      _         _        _____                          _   _            
#     / \  _   _| |_ ___ |  ___|__  _ __ _ __ ___   __ _| |_| |_ ___ _ __ 
#    / _ \| | | | __/ _ \| |_ / _ \| '__| '_ ` _ \ / _` | __| __/ _ \ '__|
#   / ___ \ |_| | || (_) |  _| (_) | |  | | | | | | (_| | |_| ||  __/ |   
#  /_/   \_\__,_|\__\___/|_|  \___/|_|  |_| |_| |_|\__,_|\__|\__\___|_|   

# ===========================================================================

# Changelog:
    # 6-17-15 - Created file [GCE]
    # 6-17-15 - Created AutoFormatter class [GCE]
    # 6-17-15 - Created Main function [GCE]
    # 6-17-15 - Added take, get, format, and getResult methods to AutoFormatter [GCE]

# ===========================================================================

# Goals:
    # Get data from Word file - COMPLETE
    # Replace symbols - COMPLETE
    # Standardize title - COMPLETE
    # Insert copyright info - COMPLETE
    # Insert indentation - COMPLETE
    # Format document to NORMAL - COMPLETE
    # Format Title with HEADING 1 - COMPLETE
    # Format Author with HEADING 2 - COMPLETE
    # Format Chapters with HEADING 2 - COMPLETE
    # Format Chapter Titles with HEADING 3 - COMPLETE
    # Search and replace "/' - MOSTLY COMPLETE/BUGGY
    # Search and replace ^13([a-z]) - COMPLETE
    # Search and replace double spaces - COMPLETE
    # Search and replace commonly mistaken puntuation - COMPLETE
    # Search and replace commonly mistaken words - COMPLETE
    # Fix italics
    # Build list of names

# ===========================================================================

# Modules
import sys
# sys.path.insert(0,"/Users/Gordon/Gordon's Files/AutoFormatter/lib")
import filelib, listlib, regexlib, doclib
import os, string
from docx import Document
from formatter import Formatter
from story import Story
from formatterApp import FormatterApp

import warnings
warnings.filterwarnings("ignore")

# ===========================================================================

def main():
    formatterApp = FormatterApp(450,450)
    formatterApp.run()
    return 0

print main()