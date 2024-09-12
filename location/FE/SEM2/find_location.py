#this file is to find location for Sem 2

#This code is to find the location of each part of F.E Sem 1

import fitz  

# Path to the PDF file
pdf_path = "uploads\FEsem1sem2.pdf"

# Open the PDF document
pdf_document = fitz.open(pdf_path)

# Define the page number (0-based index)
pdf_page = 0
page = pdf_document.load_page(pdf_page)

# Dictionary containing details for 8 subjects
subject_details = {
    #subject 1
    "code1": "101011",
    "name1": "Engineering Mechanics",
    "crd1": "M1",
    "earned1": "M2",
    "grd1": "M3",
    "gp1": "M4",
    "pnt1": "M55",
    
    #subject 2
    "code2": "101011",
    "name2": "Engineering Mechanics",
    "crd2": "M6",
    "earned2": "M7",
    "grd2": "M8",
    "gp2": "M9",
    "pnt2": "M00",
    
    #subject 3
    "code3": "102012",
    "name3": "Engineering Graphics",
    "crd3": "G1",
    "earned3": "G2",
    "grd3": "G3",
    "gp3": "G4",
    "pnt3": "G55",

    #subject 4
    "code4": "102012",
    "name4": "Engineering Graphics",
    "crd4": "G6",
    "earned4": "G7",
    "grd4": "G8",
    "gp4": "G9",
    "pnt4": "G00",

    #subject 5
    "code5": "104010",
    "name5": "Basic Electronics Engineering",
    "crd5": "X1",
    "earned5": "X2",
    "grd5": "X3",
    "gp5": "X4",
    "pnt5": "X55",

    #subject 6
    "code6": "104010",
    "name6": "Basic Electronics Engineering",
    "crd6": "X6",
    "earned6": "X7",
    "grd6": "X8",
    "gp6": "X9",
    "pnt6": "X00",

    #subject 7
    "code7": "107002",
    "name7": "Engineering Physics",
    "crd7": "P1",
    "earned7": "P2",
    "grd7": "P3",
    "gp7": "P4",
    "pnt7": "P55",

    #subject 8
    "code8": "107002",
    "name8": "Engineering Physics",
    "crd8": "P6",
    "earned8": "P7",
    "grd8": "P8",
    "gp8": "P9",
    "pnt8": "P00",


   #subject 9
    "code9": "107008",
    "name9": "Engineering Mathematics- II",
    "crd9": "T1",
    "earned9": "T2",
    "grd9": "T3",
    "gp9": "T4",
    "pnt9": "T55",

    #subject 10
    "code10": "107008",
    "name10": "Engineering Mathematics- II",
    "crd10": "T6",
    "earned10": "T7",
    "grd10": "T8",
    "gp10": "T9",
    "pnt10": "T00",


    #subject 11
    "code11": "110013",
    "name11": "Project Based Learning",
    "crd11": "B1",
    "earned11": "B2",
    "grd11": "B3",
    "gp11": "B4",
    "pnt11": "B55",


    #subject 12
    "code12": "101014",
    "name12": "Environmental Studies-II",
    "grd12": "L1",

    #subject 13
    "code13": "107015",
    "name13": " Physical Education-Exercise and Field Activities",
    "grd13": "L2",

    #subject 14
    "code14": "22295",
    "name14": "Demoracy, Election and Goveranance",
    "grd14": "L3",

    #other
    "SGPA":"7.09",
    "cred_earned": "22",
    "total_cred" : "22",
    "total_credit_pt" : "156",

}


locations = {}


for key, value in subject_details.items():
    text_instances = page.search_for(value)  # Search for the text on the page
    if text_instances:
        locations[value] = [inst for inst in text_instances]  # Store the locations of the found text
    else:
        locations[value] = 'Not found'  # If the text is not found, mark it as 'Not found'


for value, locs in locations.items():
    if locs == 'Not found':
        print(f'{value} not found.')
    else:
        print(f'{value} found at:')
        for loc in locs:
            print(f' - {loc}')

# Close the PDF document
pdf_document.close()
