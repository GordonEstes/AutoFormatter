from docx import Document
import regexlib
import string

def find(document,text):
	for paragraph in document.paragraphs:
		k = regexlib.match(paragraph.text,text)
		if k != -1: return paragraph
	return None

def replace(document,text,new):
	paragraph = find(document,text)
	if paragraph == None: return 1
	paragraph.text.replace(text,new)
	return 0

def replaceAll(document,text,new):
	while replace(document,text,new) == 0:
		continue

# Source: https://github.com/python-openxml/python-docx/issues/33#issuecomment-77661907
def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None

def mergeParagraphs(last,next):
	last.text += " "
	last.text += next.text
	delete_paragraph(next)