import fitz
from rects import rects1, rects2, rects3, rects4, rects5, rects6, rects7, rects8, rects9, rects10, rects11, rects12 , rects13

# Define the function to extract and print text from given rectangles
def extract_text_from_pdf(pdf_path, rects):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Load the first page (adjust if you need other pages)
    page = pdf_document.load_page(0)
    
    # Loop through the rectangle areas and extract text
    for key, rect in rects.items():
        text = page.get_text("text", clip=rect)
        print(f"{key}: {text.strip()}")
    
    # Close the PDF document
    pdf_document.close()

# Path to your PDF file
pdf_path = "F.E Sem1 Marksheet.pdf"

# Call the function for each set of rectangle coordinates
print("Extracting text for Subject 1:")
extract_text_from_pdf(pdf_path, rects1)

print("\nExtracting text for Subject 2:")
extract_text_from_pdf(pdf_path, rects2)

print("\nExtracting text for Subject 3:")
extract_text_from_pdf(pdf_path, rects3)

print("\nExtracting text for Subject 4:")
extract_text_from_pdf(pdf_path, rects4)

print("\nExtracting text for Subject 5:")
extract_text_from_pdf(pdf_path, rects5)

print("\nExtracting text for Subject 6:")
extract_text_from_pdf(pdf_path, rects6)

print("\nExtracting text for Subject 7:")
extract_text_from_pdf(pdf_path, rects7)

print("\nExtracting text for Subject 8:")
extract_text_from_pdf(pdf_path, rects8)

print("\nExtracting text for Subject 9:")
extract_text_from_pdf(pdf_path, rects9)

print("\nExtracting text for Subject 10:")
extract_text_from_pdf(pdf_path, rects10)

print("\nExtracting text for Subject 11:")
extract_text_from_pdf(pdf_path, rects11)

print("\nExtracting text for Subject 12:")
extract_text_from_pdf(pdf_path, rects12)

print("\nExtracting text for Other details:")
extract_text_from_pdf(pdf_path, rects13)


