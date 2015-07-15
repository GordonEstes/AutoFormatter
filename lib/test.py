# -*- coding: utf-8 -*-
import regexlib
from docx import Document



class Test(object):
    def __init__(self):
        return

    def run(self):
        document = Document('C:\Users\Gordon\Desktop\\mermaidkill.docx')
        n = 0
        for paragraph in document.paragraphs:
        	for run in paragraph.runs:
        		print run.text
        		print run.style.name
        		print run.font.italic
        		print
        		print "============="
        		print
        		n += 1
        		if n >= 50: return