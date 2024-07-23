import os
import ocrmypdf
from PIL import Image
import pytesseract
import io
import pdf2image

def extract_text_from_first_page(pdf_path):
    # Load your PDF
    pdf_file = open(pdf_path, 'rb')
    
    # Convert PDF to image
    img_pdf = pdf2image.convert_from_bytes(pdf_file.read())
    img = img_pdf[0]
    
    # Save the image as a temporary file
    img_path = os.path.join(os.path.dirname(pdf_path), "temp_image.png")
    img.save(img_path, 'PNG')
    pdf_file.close()  # Make sure to close the PDF file after reading

    # Use OCRmyPDF to enhance OCR quality and save as a new PDF
    output_pdf_path = os.path.join(os.path.dirname(pdf_path), "output.pdf")
    ocrmypdf.ocr(img_path, output_pdf_path, deskew=True, force_ocr=True, image_dpi=300)

    # Open the OCR-enhanced PDF and convert to images for text extraction
    with open(output_pdf_path, 'rb') as output_pdf:  # Use 'with' to ensure the file is properly closed after use
        output_img = pdf2image.convert_from_bytes(output_pdf.read())

    # Print the extracted text using pytesseract
    print("Text extracted using OCRmyPDF:")
    for page in output_img:
        text = pytesseract.image_to_string(page, lang='eng')
        print(text)

    # Clean up temporary files
    os.remove(img_path)
    os.remove(output_pdf_path)  # Make sure this happens after the 'with' block

# Example usage
pdf_path = 'C:\\Rohan Workplace\\AI_Paper_Classification_Agent\\aama.1993.1010.pdf'
extract_text_from_first_page(pdf_path)