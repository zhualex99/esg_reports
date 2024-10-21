import os
import spacy
from PyPDF2 import PdfReader
import re
import glob

# Replace with your folder path
path = '/Users/alexanderzhu/Library/CloudStorage/OneDrive-UniversityofWaterloo/test1' 

nlp = spacy.load("en_core_web_md")

#regex to extract the year
year_pattern = re.compile(r"\b(19|20)\d{2}\b")

# Iterate over the list of PDF files
for file in glob.glob(path + '/*.pdf'):
    print(file)
    reader = PdfReader(file)

    #extract entities from first page
    org_found = False
    year_found = False
    i = 0
    while (org_found == False or year_found == False):
        page = reader.pages[i]
        text = page.extract_text()
        doc = nlp(text)
        i+=1
        # Find named entities, phrases and concepts
        for entity in doc.ents:
            find_year = year_pattern.search(entity.text)
            if("ORG" in entity.label_):
                org = entity.text
                org_found = True
            if("DATE" in entity.label_ and find_year and len(find_year.group()) == 4 and 
                int(find_year.group()) >= 2000 and int(find_year.group()) <= 2023):
                year = find_year.group()
                year_found = True
    old_name = file
    new_name = f"{path}/{org}-{year}.pdf"

    last_4 = old_name[len(old_name)-8:len(old_name)-4]
    print(last_4)
    #renames the file only if last 4 digits don't fall into the range (2015-2022)
    #i.e. hasn't been properly named already, this is so that we don't corrupt
    #the file names that have already been manually renamed
    if(last_4 < "2015" or last_4 > "2022"):
        os.rename(old_name,new_name)


#Assumptions made:
#File names are at least 4 characters long, followed by .pdf
#File names ending in 2015-2022 have already been renamed