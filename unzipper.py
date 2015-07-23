import zipfile
from lxml import etree

def getXml(docxFilename):
    zip = zipfile.ZipFile(open(docxFilename))
    xmlContent = zip.read("word/document.xml")
    return xmlContent

def getXmlTree(xmlContent):
    return etree.fromstring(xmlContent)

testXml = getXml("test.docx")
print(getXmlTree(testXml))