import fitz

pdf_path = "F.E Sem1 Marksheet.pdf"
pdf_document =  fitz.open(pdf_path)

page = pdf_document.load_page(0)

text = page.search_for("Systems in Mechanical Engineering")

if text:
    rect = text[0]
    print(f"Text found at coordinates: {rect}")
else:
    print("Text not found.")