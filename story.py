# -*- coding: utf-8 -*-

import sys
# sys.path.insert(0,"/Users/Gordon/Gordon's Files/AutoFormatter/lib")
import filelib, listlib, regexlib
import os, string

class Story(object):
    def __init__(self,title,author,path,copyright="",publisher=""):
        self.title = title
        self.author = author
        self.copyright = copyright
        self.publisher = publisher
        self.path = path

    def getPath(self):
        return self.path

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getCopyright(self):
        if self.copyright == "":
            return None
        return self.copyright

    def getPublisher(self):
        if self.publisher == "":
            return None
        return self.publisher

    def duplicate(self):
        copy = Story(self.title,self.author,self.path,self.copyright,self.publisher)
        return copy