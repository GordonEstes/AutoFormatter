# -*- coding: utf-8 -*-

import zipfile
import os
import tempfile
import shutil
import io

def getXml(docxFilename): #Extracts the XML from docxFilename as a string
    zip = zipfile.ZipFile(open(docxFilename,"rb"))
    xmlString= zip.read("word/document.xml").decode("utf-8")
    return xmlString

def createNewDocx(originalDocx,xmlString,newFilename): #Takes the original Word doc and replaces its XML with xmlString, saving it as newFilename
    tmpDir = tempfile.mkdtemp()
    zip = zipfile.ZipFile(open(originalDocx,"rb"))
    zip.extractall(tmpDir)
    with io.open(os.path.join(tmpDir, "word/document.xml"), "w", encoding="UTF-8") as f:
        f.write(xmlString)
    filenames = zip.namelist()
    zipCopyFilename = newFilename
    with zipfile.ZipFile(zipCopyFilename,"w") as docx:
        for filename in filenames:
            docx.write(os.path.join(tmpDir,filename),filename)
    shutil.rmtree(tmpDir)

def rmTo(text,i,k):
    new = text[i:]
    j = new.find(k)
    return text[:i] + "\n" + new[j+len(k):]


def rmSmartTag(xmlString):
    i = xmlString.find("<w:smartTag")
    while i != -1:
        xmlString = rmTo(xmlString,i,">")
        i = xmlString.find("<w:smartTag")
    i = xmlString.find("</w:smartTag")
    while i != -1:
        xmlString = rmTo(xmlString,i,">")
        i = xmlString.find("</w:smartTag")
    return xmlString

# xmlString = '</w:t></w:r><w:smartTag w:uri="urn:schemas-microsoft-com:office:smarttags" w:element="place"><w:smartTag w:uri="urn:schemas-microsoft-com:office:smarttags" w:element="PlaceName"><w:r><w:rPr><w:rStyle w:val="Bodytext2"/><w:color w:val="000000"/></w:rPr><w:t>Bronx</w:t></w:r></w:smartTag><w:r><w:rPr><w:rStyle w:val="Bodytext2"/><w:color w:val="000000"/></w:rPr><w:t xml:space="preserve"> </w:t></w:r><w:smartTag w:uri="urn:schemas-microsoft-com:office:smarttags" w:element="PlaceType"><w:r><w:rPr><w:rStyle w:val="Bodytext2"/><w:color w:val="000000"/></w:rPr><w:t>Park</w:t></w:r></w:smartTag></w:smartTag><w:r><w:rPr><w:rStyle w:val="Bodytext2"/><w:color w:val="000000"/></w:rPr><w:t xml:space="preserve"> which opened that morning, for—”</w:t></w:r></w:p><w:p w:rsidR="002A3EEE" w:rsidRDefault="002A3EEE" w:rsidP="002A3EEE"><w:pPr><w:pStyle w:val="Bodytext21"/><w:shd w:val="clear" w:color="auto" w:fill="'
# print rmSmartTag(xmlString)

def fixXML(path):
    xmlString = getXml(path)
    xmlString = rmSmartTag(xmlString)
    createNewDocx(path,xmlString,path)

# path = "C:\Users\Gordon\Desktop\punchbowl_shortened.docx"
# fixXML(path)

# xmlString = getXml("C:\Users\Gordon\Desktop\punchbowl_shortened.docx")
# xmlString = rmSmartTag(xmlString)
# createNewDocx("C:\Users\Gordon\Desktop\punchbowl_shortened.docx",xmlString,"C:\Users\Gordon\Desktop\punch_short2.docx")

# createNewDocx("16Beans.docx",getXml("16Beans.docx"),"beans2.docx")
