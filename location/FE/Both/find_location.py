import fitz 
pdf_path = "location\FE\Both\SEM1&SEM2.pdf"

# Open the PDF document
pdf_document = fitz.open(pdf_path)

pdf_page = 0
page = pdf_document.load_page(pdf_page)


sem1 = {
        "code1": "102003",
        "name1": "Systems in Mechanical Engineering",
        "crd1": "S1",
        "earned1": "S2",
        "grd1": "S3",
        "gp1": "S4",
        "pnt1": "S55",
    
    #subject 2
    "code2": "102003",
    "name2": "Systems in Mechanical Engineering",
    "crd2": "S6",
    "earned2": "S7",
    "grd2": "S8",
    "gp2": "S9",
    "pnt2": "S00",
    
    #subject 3
    "code3": "103004",
    "name3": " Basic Electrical Engineering",
    "crd3": "B1",
    "earned3": "B2",
    "grd3": "B3",
    "gp3": "B4",
    "pnt3": "B55",

    #subject 4
    "code4": "103004",
    "name4": "Basic Electrical Engineering",
    "crd4": "B6",
    "earned4": "B7",
    "grd4": "B8",
    "gp4": "B9",
    "pnt4": "B00",

    #subject 5
    "code5": "107001",
    "name5": " Engineering Mathematics-I",
    "crd5": "M1",
    "earned5": "M2",
    "grd5": "M3",
    "gp5": "M4",
    "pnt5": "M55",

    #subject 6
    "code6": "107001",
    "name6": "Engineering Mathematics-I",
    "crd6": "M6",
    "earned6": "M7",
    "grd6": "M8",
    "gp6": "M9",
    "pnt6": "M00",

    #subject 7
    "code7": "107009",
    "name7": " Engineering Chemistry",
    "crd7": "C1",
    "earned7": "C2",
    "grd7": "C3",
    "gp7": "C4",
    "pnt7": "C55",

    #subject 8
    "code8": "107009",
    "name8": "Engineering Chemistry",
    "crd8": "C6",
    "earned8": "C7",
    "grd8": "C8",
    "gp8": "C9",
    "pnt8": "C00",

    #subject 9
    "code9": "110005",
    "name9": "Programming and Problem Solving",
    "crd9": "P1",
    "earned9": "P2",
    "grd9": "P3",
    "gp9": "P4",
    "pnt9": "P55",

    #subject 10
    "code10": "110005",
    "name10": " Programming and Problem Solving",
    "crd10": "P6",
    "earned10": "P7",
    "grd10": "P8",
    "gp10": "P9",
    "pnt10": "P00",

    #subject 11
    "code11": "111006",
    "name11": "Workshop",
    "crd11": "W1",
    "earned11": "W2",
    "grd11": "W3",
    "gp11": "W4",
    "pnt11": "W55",

    #subject 12
    "code12": "101007",
    "name12": "Environmental Studies-I",
    "grd12": "L1",

    #other
    "SGPA":"7.86",
    "cred_earned": "22",
    "total_cred" : "22",
    "total_credit_pt" : "173",

}


sem2 = {
    #subject 1
    "code1": "101011",
    "name1": "Engineering Mechanics",
    "crd1": "H1",
    "earned1": "H2",
    "grd1": "H3",
    "gp1": "H4",
    "pnt1": "H55",

    #subject 2
    "code2": "101011",
    "name2": "Engineering Mechanics",
    "crd2": "H6",
    "earned2": "H7",
    "grd2": "H8",
    "gp2": "H9",
    "pnt2": "H00",

    
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
    "crd7": "Y1",
    "earned7": "Y2",
    "grd7": "Y3",
    "gp7": "Y4",
    "pnt7": "Y55",

    #subject 8
    "code8": "107002",
    "name8": "Engineering Physics",
    "crd8": "Y6",
    "earned8": "Y7",
    "grd8": "Y8",
    "gp8": "Y9",
    "pnt8": "Y00",

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




locations_sem1 = {}


for key, value in sem1.items():
    text_instances = page.search_for(value)  # Search for the text on the page
    if text_instances:
        locations_sem1[value] = [inst for inst in text_instances]  # Store the locations of the found text
    else:
        locations_sem1[value] = 'Not found'  # If the text is not found, mark it as 'Not found'


for value, locs in locations_sem1.items():
    if locs == 'Not found':
        print(f'{value} not found.')
    else:
        print(f'{value} found at:')
        for loc in locs:
            print(f' - {loc}')


locations_sem2= {}


for key, value in locations_sem2.items():
    text_instances = page.search_for(value)  # Search for the text on the page
    if text_instances:
        locations_sem2[value] = [inst for inst in text_instances]  # Store the locations of the found text
    else:
        locations_sem2[value] = 'Not found'  # If the text is not found, mark it as 'Not found'


for value, locs in locations_sem2.items():
    if locs == 'Not found':
        print(f'{value} not found.')
    else:
        print(f'{value} found at:')
        for loc in locs:
            print(f' - {loc}')

# Close the PDF document
pdf_document.close()

