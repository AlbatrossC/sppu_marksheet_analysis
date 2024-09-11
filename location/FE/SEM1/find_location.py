#This code is to find the location of each part of F.E Sem 1

import fitz  # PyMuPDF

# Path to the PDF file
pdf_path = "location\location.pdf"

# Open the PDF document
pdf_document = fitz.open(pdf_path)

# Define the page number (0-based index)
pdf_page = 0
page = pdf_document.load_page(pdf_page)

# Dictionary containing details for 8 subjects
subject_details = {
    #subject 1
    "code1": "* 102003-1 ",
    "name1": "Systems in Mechanical Engineering",
    "crd1": "S1",
    "earned1": "S2",
    "grd1": "S3",
    "gp1": "S4",
    "pnt1": "S55",
    
    #subject 2
    "code2": "* 102003-1_PR",
    "name2": "Systems in Mechanical Engineering",
    "crd2": "S6",
    "earned2": "S7",
    "grd2": "S8",
    "gp2": "S9",
    "pnt2": "S00",
    
    #subject 3
    "code3": "* 103004-1",
    "name3": " Basic Electrical Engineering",
    "crd3": "B1",
    "earned3": "B2",
    "grd3": "B3",
    "gp3": "B4",
    "pnt3": "B55",

    #subject 4
    "code4": "* 103004-1_PR",
    "name4": "Basic Electrical Engineering",
    "crd4": "B6",
    "earned4": "B7",
    "grd4": "B8",
    "gp4": "B9",
    "pnt4": "B00",

    #subject 5
    "code5": "* 107001",
    "name5": " Engineering Mathematics-I",
    "crd5": "M1",
    "earned5": "M2",
    "grd5": "M3",
    "gp5": "M4",
    "pnt5": "M55",

    #subject 6
    "code6": "* 107001_TW",
    "name6": "Engineering Mathematics-I",
    "crd6": "M6",
    "earned6": "M7",
    "grd6": "M8",
    "gp6": "M9",
    "pnt6": "M00",

    #subject 7
    "code7": "* 107009-1",
    "name7": " Engineering Chemistry",
    "crd7": "C1",
    "earned7": "C2",
    "grd7": "C3",
    "gp7": "C4",
    "pnt7": "C55",

    #subject 8
    "code8": "107009-1_PR",
    "name8": "Engineering Chemistry",
    "crd8": "C6",
    "earned8": "C7",
    "grd8": "C8",
    "gp8": "C9",
    "pnt8": "C00",

    #subject 9
    "code9": "* 110005-1",
    "name9": "Programming and Problem Solving",
    "crd9": "P1",
    "earned9": "P2",
    "grd9": "P3",
    "gp9": "P4",
    "pnt9": "P55",

    #subject 10
    "code10": "* 110005-1_PR",
    "name10": " Programming and Problem Solving",
    "crd10": "P6",
    "earned10": "P7",
    "grd10": "P8",
    "gp10": "P9",
    "pnt10": "P00",

    #subject 11
    "code11": "* 111006",
    "name11": "Workshop",
    "crd11": "W1",
    "earned11": "W2",
    "grd11": "W3",
    "gp11": "W4",
    "pnt11": "W55",

    #subject 12
    "code12": "* 101007",
    "name12": "Environmental Studies-I",
    "grd12": "EVS",

    #other
    "SGPA":"7.86",
    "cred_earned": "22",
    "total_cred" : "22",
    "total_credit_pt" : "173",

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
