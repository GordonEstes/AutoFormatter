# -*- coding: utf-8 -*-

# ===========================================================================

#      _         _        _____                          _   _            
#     / \  _   _| |_ ___ |  ___|__  _ __ _ __ ___   __ _| |_| |_ ___ _ __ 
#    / _ \| | | | __/ _ \| |_ / _ \| '__| '_ ` _ \ / _` | __| __/ _ \ '__|
#   / ___ \ |_| | || (_) |  _| (_) | |  | | | | | | (_| | |_| ||  __/ |   
#  /_/   \_\__,_|\__\___/|_|  \___/|_|  |_| |_| |_|\__,_|\__|\__\___|_|   

# ===========================================================================

# Modules
import sys
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