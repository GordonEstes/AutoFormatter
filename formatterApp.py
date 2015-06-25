# -*- coding: utf-8 -*-

import sys
# sys.path.insert(0,"/Users/Gordon/Gordon's Files/AutoFormatter/lib")
import filelib, listlib, regexlib
import os, string
from eventBasedAnimationClass import EventBasedAnimationClass
from Tkinter import *
# import PIL
# from PIL import Image, ImageTk
import tkFileDialog
from formatter import Formatter
from docx import Document
from formatter import Formatter
from story import Story
from struct import Struct
import thread

class FormatterApp(EventBasedAnimationClass):
    def __init__(self,width,height):
        self.width = 480
        self.height = 360
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.buttons = {}
        self.textBoxes = {}
        self.checkBoxes = {}
        self.path=""
        self.formatter = Formatter()
        self.running = False

    # Initializes the animation attributes.
    def initAnimation(self):
        self.timerDelay = 100 #milliseconds
        self.initButtons()
        self.initText()
        self.initCheckBoxes()
        self.root.wm_title("AutoFormatter")
        self.canvas.v = IntVar()

    def onTimerFired(self):
        if self.running and self.formatter.stage == "Complete":
            self.running = False
            self.formatter.stage = "Incomplete"

    def quit(self):
        self.root.destroy()

    def browse(self):
        filename = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
        path = filename.name
        print path
        filename.close()
        self.path = path

    def go(self):
        title = self.textBoxes["Title"].get("1.0",'end-1c')
        author = self.textBoxes["Author"].get("1.0",'end-1c')
        publisher = self.textBoxes["Publisher"].get("1.0",'end-1c')
        copyright = self.textBoxes["Copyright"].get("1.0",'end-1c')
        newStory = Story(title,author,self.path,copyright,publisher)
        chapterTitles = self.checkBoxes["Titles"]
        self.formatter.chapterNames = bool(self.var.get())
        self.formatter.take(newStory)
        self.running = True
        self.formatThread = thread.start_new_thread(self.formatter.run, ())

    def initButtons(self):
        quit = Button(self.canvas,text="Quit",command=self.quit,width=6,height=1)
        self.buttons["Quit"] = quit
        browse = Button(self.canvas,text="Browse",command=self.browse,width=6,height=1,anchor="e")
        self.buttons["Browse"] = browse
        go = Button(self.canvas,text="Go",command=self.go,width=6,height=1)
        self.buttons["Go"] = go

    def initCheckBoxes(self):
        self.var = IntVar()
        chapterTitles = Checkbutton(self.canvas,text="Use chapter titles",variable=self.var)
        self.checkBoxes["Titles"] = chapterTitles

    def initText(self):
        height = 1
        width = 35
        title = Text(self.root,height=height,width=width)
        self.textBoxes["Title"] = title
        author = Text(self.root,height=height,width=width)
        self.textBoxes["Author"] = author
        publisher = Text(self.root,height=height,width=width)
        self.textBoxes["Publisher"] = publisher
        copyright = Text(self.root,height=height,width=width)
        self.textBoxes["Copyright"] = copyright

    def drawBackground(self):
        width = self.width
        height = self.height
        background = self.canvas.create_rectangle(0,0,width,height,fill="bisque3")

    def create(self,width,height,window):
        self.canvas.create_window(width,height,window=window)

    def drawBar(self):
        self.canvas.create_window(self.width*1/2,self.height*1/4,window=self.bar)

    def drawButtons(self):
        w = self.width
        h = self.height
        if self.running:
            pass
        else:
            quit = self.buttons["Quit"]
            browse = self.buttons["Browse"]
            go = self.buttons["Go"]
            self.create(w*1/8,h*7/8,go)
            self.create(w*1/8,h*6/8,browse)
            self.create(w*2/8,h*7/8,quit)

    def drawTextBoxes(self):
        w = self.width
        h = self.height
        if self.running:
            pass
        else:
            title = self.textBoxes["Title"]
            author = self.textBoxes["Author"]
            publisher = self.textBoxes["Publisher"]
            copyright = self.textBoxes["Copyright"]
            self.canvas.create_window(w*1.5/8,h*1/8,window=title,anchor="w")
            self.canvas.create_window(w*1.5/8,h*2/8,window=author,anchor="w")
            self.canvas.create_window(w*1.5/8,h*3/8,window=publisher,anchor="w")
            self.canvas.create_window(w*1.5/8,h*4/8,window=copyright,anchor="w")        

    def drawText(self):
        w = self.width
        h = self.height
        if self.running:
            progress = self.canvas.create_text(w*4/8,h*4/8,text=self.formatter.progress)
        else:
            title = self.canvas.create_text(w*1.25/8,h*1/8,text="Title:",anchor="e")
            author = self.canvas.create_text(w*1.25/8,h*2/8,text="Author:",anchor="e")
            publisher = self.canvas.create_text(w*1.25/8,h*3/8,text="Publisher:",anchor="e")
            copyright = self.canvas.create_text(w*1.25/8,h*4/8,text="Copyright:",anchor="e")
            path = self.canvas.create_text(w*1.5/8,h*6/8,text="Path: %s" % self.path,anchor="w")

    def drawProgressBar(self):
        w = self.width
        h = self.height
        if self.running:
            (x1,x2) = (w*1/4,w*3/4)
            (y1,y2) = (h*2/8,h*3/8)
            (z1,z2) = (x1-5,x2+5)
            (n1,n2) = (y1-5,y2+5)
            color = "green yellow"
            percent = 0 if (self.formatter.steps == 0) else (self.formatter.step/self.formatter.steps)
            x2 = (x2-x1) * percent + x1
            if self.running:
                backBar = self.canvas.create_rectangle(z1,n1,z2,n2,fill="gray70")
                progressBar = self.canvas.create_rectangle(x1,y1,x2,y2,fill=color)

    def drawCheckButtons(self):
        w = self.width
        h = self.height
        if self.running:
            pass
        else:
            chapterTitles = self.checkBoxes["Titles"]
            self.canvas.create_window(w*2/8,h*5/8,window=chapterTitles)

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawBackground()
        self.drawButtons()
        self.drawTextBoxes()
        self.drawProgressBar()
        self.drawText()
        self.drawCheckButtons()