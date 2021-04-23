import pdfplumber


pdf = pdfplumber.open('U.S._History.pdf')
text = ""
pages = pdf.pages
for page in pages:
    if (type(page.extract_text()) is str):
        text = text + page.extract_text(x_tolerance=0.5)
pdf.close()

with open("usHistory.txt", "w") as f:
    f.write(text)

