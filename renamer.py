import os
import spacy
import PyPDF2
from PyPDF2 import PdfReader
import re

nlp = spacy.load("en_core_web_sm")

path = 'Greene King - 2014.pdf'
reader = PdfReader(path)
number_of_pages = len(reader.pages)

page = reader.pages[0]
text = page.extract_text()

doc = nlp(text)

#initialize the key global variables
org = ''
year = ''

#regex to extract the year
year_pattern = re.compile(r"\b(19|20)\d{2}\b")

print(doc.ents)
# Find named entities, phrases and concepts
for entity in doc.ents:
    if("ORG" in entity.label_):
        org = entity.text
    if("DATE" in entity.label_):
        #fixes bug where sometimes date has additional numbers after a space
        #if(len(entity.text) == 4): 
        year = year_pattern.search(entity.text).group()

new_name = f"will be renamed to: {org}-{year}"
print(new_name)