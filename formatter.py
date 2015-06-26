# -*- coding: utf-8 -*-

################
# BUGS:
    # initStyles does not properly initialize the font ("Arial" stays as "Calibri")
    # Other stuff
    # Other stuff
################

import sys
# sys.path.insert(0,"/Users/Gordon/Gordon's Files/AutoFormatter/lib")
import filelib, listlib, regexlib, doclib, numlib
import os, string
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
import unicodedata
from docx.shared import Inches
from docx.shared import Pt
from story import Story
import Tkinter as tk

# The Formatter is an object that is able to take in a Story object and return a properly
# formatted version.
class Formatter(object):

    # Initializes the values used by the Formatter.
    def __init__(self):
        self.legalChars = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!#$%&*()_+=;:'\"/?.,—<>“”’ "
        self.story = None
        self.document1 = None
        self.document2 = None
        self.chapterNames = True
        self.progress = "Waiting for input."
        self.stage = "Incomplete"
        self.step = 0.0
        self.steps = 0.0
        self.gettingSize = False
        self.paragraphDict = {}
        
    def initStyles(self):
        self.progress = "Initializing styles..."
        styles = self.document2.styles

        styles["Heading 1"].font.name = "Arial"
        styles["Heading 1"].font.size = Pt(16)
        styles["Heading 1"].font.color.rgb = None 
        styles["Heading 1"].font.bold = True
        styles["Heading 1"].paragraph_format.first_line_indent = Inches(0.5)

        styles["Heading 2"].font.name = "Arial"
        styles["Heading 2"].font.size = Pt(14)
        styles["Heading 2"].font.color.rgb = None 
        styles["Heading 2"].font.bold = True
        styles["Heading 2"].font.italic = True
        styles["Heading 2"].paragraph_format.first_line_indent = Inches(0.5)

        styles["Heading 3"].font.name = "Arial"
        styles["Heading 3"].font.size = Pt(13)
        styles["Heading 3"].font.color.rgb = None 
        styles["Heading 3"].font.bold = True
        styles["Heading 3"].paragraph_format.first_line_indent = Inches(0.5)

        styles["Normal"].font.name = "Times New Roman"
        styles["Normal"].font.size = Pt(14)
        styles["Normal"].font.color.rgb = None 
        styles["Normal"].paragraph_format.first_line_indent = Inches(0.5)

    # Takes in an object representing the story to be formatted and sets the local
    # story value to equal it.
    def take(self,story):
        self.progress = "Taking an unformatted story..."
        self.story = story
        self.document1 = Document(story.path)
        self.document2 = Document()
        self.initStyles()

    def save(self):
        self.progress = "Saving formatted document..."
        path = self.story.path
        document = self.document2
        path = regexlib.clipRight(path,".")
        path += "_formatted.docx"
        document.save(path)

    def build(self):
        self.progress = "Building document..."
        document1 = self.document1
        document2 = self.document2
        paragraph_format = document2.styles['Normal'].paragraph_format
        paragraph_format.space_before = 0 #Set paragraph spacing to 0 pica.
        paragraph_format.space_after = 0 
        for p1 in document1.paragraphs: #Copy each paragraph from document1 to document 2.
            p2 = document2.add_paragraph(p1.text)
            self.paragraphDict[p1.text] = p2

    def removeSymbols(self):
        if not self.gettingSize: self.progress = "Removing symbols..."
        document2 = self.document2
        for paragraph in document2.paragraphs:
            text = paragraph.text
            text = text.replace(u"—","---")
            text = regexlib.removeAll(text,"»")
            text = regexlib.removeAll(text,"|")
            text = regexlib.removeAll(text,"«")
            text = regexlib.removeAll(text,"•")
            text = regexlib.removeAll(text,"    ")
            paragraph.text = text
            self.step += 1

    def insertTitle(self):
        if not self.gettingSize: self.progress = self.progress = "Adding title..."
        title = self.story.title
        style = 'Heading 1'
        self.document2.paragraphs[0].insert_paragraph_before(title,style)

    def insertAuthor(self):
        if not self.gettingSize: self.progress = self.progress = "Adding author..."
        author = self.story.author
        style = 'Heading 2'
        self.document2.paragraphs[1].insert_paragraph_before(author,style)

    def insertCopyright(self):
        if not self.gettingSize: self.progress = self.progress = "Adding copyright..."
        copyright = self.story.copyright
        if copyright == "": return
        paragraph = self.document2.paragraphs[2]
        copyrightParagraph = paragraph.insert_paragraph_before("")
        copyrightParagraph.add_run("(copyright %s)" % copyright).italic = True

    def insertPublisher(self):
        if not self.gettingSize: self.progress = self.progress = "Adding publisher..."
        publisher = self.story.publisher
        if publisher == "": return
        paragraph = self.document2.paragraphs[2]
        publisherParagraph = paragraph.insert_paragraph_before("")
        publisherParagraph.add_run("(publisher %s)" % publisher).italic = True

    def formatChapters(self):
        if not self.gettingSize: self.progress = "Formatting chapters..."
        chapter = False
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            if ("Chapter" or "CHAPTER" or "BOOK" or "Book") in text:
                if len(text) <= len("Chapter XXXXIIII"):
                   chapter = True
                   paragraph.style = 'Heading 2'
            elif chapter and self.chapterNames:
                paragraph.style = 'Heading 3'
                chapter = False
            else:
                chapter = False
            self.step += 1

    def fixDoubleQuotes(self):
        if not self.gettingSize: self.progress = "Fixing double quotes..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            i = regexlib.match(text,u'” “')  
            if i == -1: i = regexlib.match(text,'" "')      
            if i != -1:
                text1 = text[:i+1]
                text2 = text[i+2:]
                paragraph.text = text2
                paragraph.insert_paragraph_before(text1)
            self.step += 1

    def convertPunctuation(self):
        if not self.gettingSize: self.progress = "Converting punctuation..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            punctuation = { 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22 }
            text = u'%s' % text
            text = text.translate(punctuation).encode('ascii', 'ignore')
            paragraph.text = text
            self.step += 1

    def fixEmDash(self):
        if not self.gettingSize: self.progress = "Fixing em-dashes..."
        document2 = self.document2
        for paragraph in document2.paragraphs:
            text = paragraph.text
            text = text.replace('---"',u'---”')
            text = text.replace('"---',u'“---')
            text = text.replace("---",u"—")
            text = regexlib.replaceSub(text," — ","—")
            text = regexlib.replaceSub(text," —","—")
            text = regexlib.replaceSub(text,"— ","—")
            paragraph.text = text
            self.step += 1

    def fixQuotations(self):
        if not self.gettingSize: self.progress = "Fixing quotations..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            text = regexlib.replaceSub(text,', said','," said')
            text = regexlib.replaceSub(text,' "',u' “')
            text = regexlib.replaceSub(text,'" ',u'” ')
            text = regexlib.replaceSub(text,'."',u'.”')
            text = regexlib.replaceSub(text,',"',u',”')
            text = regexlib.replaceSub(text,'!"',u'!”')
            text = regexlib.replaceSub(text,'?"',u'?”')
            text = regexlib.replaceSub(text,'..."',u'...”')
            text = regexlib.replaceSub(text,'—"',u'—”')
            text = regexlib.replaceSub(text,'’"',u'’”')
            text = regexlib.replaceSub(text,'\'"',u'’”')
            text = regexlib.replaceSub(text,'"',u'“')
            paragraph.text = text
            self.step += 1

    def fixCaps(self):
        if not self.gettingSize: 
            self.progress = "Fixing chapter capitalization..."
        for paragraph in self.document2.paragraphs:
            if len(paragraph.text) < 2: 
                continue
            if paragraph.style.name != "Normal":
                continue
            if (paragraph.text[0] in string.ascii_uppercase
            and paragraph.text[1] in string.ascii_uppercase
            and paragraph.text[2] in string.ascii_uppercase):
                s = paragraph.text
                for i in xrange(1,len(s)):
                    if s[i] in string.ascii_lowercase: break
                    if s[i] in string.ascii_uppercase:
                        s = regexlib.replaceIndex(s,i,string.lower(s[i]))
                paragraph.text = s
            self.step += 1

    def fixCarriageReturn(self):
        if not self.gettingSize: self.progress = "Fixing carriage returns..."
        last = None
        for paragraph in self.document2.paragraphs:
            if paragraph == self.document2.paragraphs[0]: continue
            text = paragraph.text
            if last != None and len(text) >= 1 and text[0] in " qwertyuiopasdfghjklzxcvbnm":
                doclib.mergeParagraphs(last,paragraph)
            else:
                last = paragraph
            self.step += 1

    def fixApostrophes(self):
        if not self.gettingSize: self.progress = "Fixing apostrophes..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            text = regexlib.replaceSub(text,"''","\"")
            text = regexlib.replaceSub(text," '",u' ‘')
            text = regexlib.replaceSub(text,"' ",u'’ ')
            text = regexlib.replaceSub(text,".'",u'.’')
            text = regexlib.replaceSub(text,",'",u',’')
            text = regexlib.replaceSub(text,"!'",u'!’')
            text = regexlib.replaceSub(text,"?'",u'?’')
            text = regexlib.replaceSub(text,"...'",u'...’')
            text = regexlib.replaceSub(text,"—'",u'—’')
            text = regexlib.replaceSub(text,"'.",u'’.')
            text = regexlib.replaceSub(text,"',",u'’,')
            text = regexlib.replaceSub(text,"'!",u'’!')
            text = regexlib.replaceSub(text,"'?",u'’?')
            text = regexlib.replaceSub(text,"'...",u'’...')
            text = regexlib.replaceSub(text,"'—",u'’—')
            text = regexlib.replaceSub(text,"#'#",u'#’#')
            text = regexlib.replaceSub(text,"'",u'‘')
            paragraph.text = text
            self.step += 1

    def fixDoubleSpace(self):
        if not self.gettingSize: self.progress = "Fixing double spaces..."
        for paragraph in self.document2.paragraphs:
            while regexlib.match(paragraph.text, "  ") != -1:
                paragraph.text = regexlib.replaceSub(paragraph.text, "  ", " ")
            self.step += 1

    def fixEllipses(self):
        if not self.gettingSize: self.progress = "Fixing ellipses..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            text = regexlib.replaceSub(text," . . . . .", "...")
            text = regexlib.replaceSub(text," . . . .","...")
            text = regexlib.replaceSub(text," . . .","...")
            text = regexlib.replaceSub(text,". . . . .", "...")
            text = regexlib.replaceSub(text,". . . .","...")
            text = regexlib.replaceSub(text,". . .","...")
            text = regexlib.replaceSub(text,".....","...")
            text = regexlib.replaceSub(text,"....","...")
            text = regexlib.replaceSub(text," . .",u'...”')
            text = regexlib.replaceSub(text,". . ",u"“...")
            paragraph.text = text   
            self.step += 1  

    def fixPunctuation(self):
        if not self.gettingSize: self.progress = "Fixing punctuation..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            #Hyphens
            text = regexlib.removeSub(text," -")
            text = regexlib.replaceSub(text,"- ","-")
            #Misc
            text = regexlib.replaceSub(text,"/","I")
            text = regexlib.removeSub(text,"\\")
            text = regexlib.removeSub(text,"^")
            #Asterisks
            text = regexlib.replaceSub(text,"* * * *", "& & & &")
            text = regexlib.removeSub(text,"*")
            text = regexlib.replaceSub(text,"& & & &", "* * * *")
            paragraph.text = text
            self.step += 1

    def fixWords(self):
        if not self.gettingSize: self.progress = "Fixing words..."
        for paragraph in self.document2.paragraphs:
            text = paragraph.text
            text = regexlib.replaceWord(text,"comer","corner")
            text = regexlib.replaceWord(text,"bom","born")
            text = regexlib.replaceWord(text,"modem","modern")
            text = regexlib.replaceWord(text,"tiling","thing")
            text = regexlib.replaceWord(text,"diat","that")
            text = regexlib.replaceWord(text,"sec","see")
            text = regexlib.replaceWord(text,"secs","sees")
            text = regexlib.replaceWord(text,"Fd","I'd")
            paragraph.text = text
            self.step += 1

    def getSize(self):
        self.progress = "Getting document size..."
        document2 = self.document2
        self.document2 = Document()
        for paragraph in self.document1.paragraphs: self.document2.add_paragraph("")
        self.gettingSize = True
        self.format()
        self.fix()
        self.gettingSize = False
        self.steps = self.step
        self.step = 0.0
        self.document2 = document2

    def formatChapterBreaks(self):
        if not self.gettingSize: self.progress = "Separating chapters..."
        for paragraph in self.document2.paragraphs:
            if paragraph.text == "* * * *":
                text = ""
                style = "Normal"
                paragraph_1 = paragraph.insert_paragraph_before(text,style)
                paragraph_2 = paragraph.insert_paragraph_before(paragraph.text,style)
                paragraph_2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.text = ""
            self.step += 1

    def fixItalics(self):
        self.progress = "Fixing italics..."
        print self.progress
        for p1 in self.document1.paragraphs:
            p2 = self.paragraphDict[p1.text]
            for r1 in p1.runs:
                if r1.italic or "Italic" in r1.style.name:
                    i = regexlib.match(p2.text,r1.text)
                    if i == -1: continue
                    r2a = p2.text[:i]
                    r2b = p2.text[i:i+len(r1.text)]
                    r2c = p2.text[i+len(r1.text):]
                    p2.text = r2a
                    r2b = p2.add_run(r2b)
                    p2.add_run(r2c)
                    r2b.italic = True
            self.step += 4

    def fix(self):
        if not self.gettingSize: self.progress = "Fixing mistakes..."
        self.fixEmDash()
        self.fixDoubleQuotes()
        self.fixApostrophes()
        self.fixQuotations()
        self.fixDoubleSpace()
        self.fixEllipses()
        self.fixPunctuation()
        self.fixWords()
        self.fixCaps()
        self.fixItalics()
        self.fixDoubleQuotes()
        self.fixCarriageReturn()
        self.formatChapterBreaks()
        self.insertTitle()
        self.insertAuthor()
        self.insertCopyright()
        self.insertPublisher()

    def format(self):
        if not self.gettingSize: self.progress = "Formatting story..."
        self.removeSymbols()
        self.formatChapters()
        self.convertPunctuation()

    def open(self):
        self.progress = "Opening file..."
        path = self.story.path
        path = regexlib.clipRight(path,".")
        path += "_formatted.docx"
        os.system("start "+path)

    # Sets the local result variable by processing the local story variable.
    def run(self):
        self.progress = "Running formatter..."
        sys.stdout.flush()
        self.build()
        self.getSize()
        self.format()
        self.fix()
        self.save()
        self.stage = "Complete"
        self.open()
        self.step = 0.0
