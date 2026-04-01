from pypdf import PdfReader
reader = PdfReader('Projet mi-guidé Django python.pdf')
with open('output.txt', 'w', encoding='utf-8') as f:
    for page in reader.pages:
        f.write(page.extract_text() + '\n\n')
