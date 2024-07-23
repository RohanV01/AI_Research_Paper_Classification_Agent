import fitz  # Import PyMuPDF

def extract_text_from_first_page(pdf_path):
    doc = fitz.open(pdf_path)
    
    if len(doc) > 0:
        first_page_text = doc[0].get_text()
    else:
        first_page_text = "No pages in PDF."

    doc.close()

    return first_page_text

# Example usage
pdf_path = 'C:\\Users\\user\\Desktop\\test_pdfs\\aama.1993.1009.pdf'  # Replace this with the path to your PDF file
print(extract_text_from_first_page(pdf_path))
