import fitz

pdf_path = "F.E Sem1 Marksheet.pdf"
pdf_document = fitz.open(pdf_path)

page = pdf_document.load_page(0)

rect = fitz.Rect(157.62344360351562, 219.73904418945312, 315.9976806640625, 233.47767639160156)
text = page.get_text("text", clip=rect)

print(text)
pdf_document.close()