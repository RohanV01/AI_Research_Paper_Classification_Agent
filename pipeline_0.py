import os
import shutil
import fitz  # PyMuPDF
import ocrmypdf
import pytesseract
import pdf2image
import logging
import time
import datetime
from openai import OpenAI

# Setup logging with a unique filename based on the current timestamp
log_filename = f"process_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(filename=log_filename, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_first_page(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = doc[0].get_text() if len(doc) > 0 else ""
        doc.close()
        if not text:  # If no text was extracted using PyMuPDF, use OCR
            pdf_file = open(pdf_path, 'rb')
            img_pdf = pdf2image.convert_from_bytes(pdf_file.read())
            img = img_pdf[0]
            img_path = os.path.join(os.path.dirname(pdf_path), "temp_image.png")
            img.save(img_path, 'PNG')
            pdf_file.close()  # Ensure PDF file is closed after reading

            # Use OCRmyPDF for OCR and save as a new PDF
            output_pdf_path = os.path.join(os.path.dirname(pdf_path), "output.pdf")
            ocrmypdf.ocr(img_path, output_pdf_path, deskew=True, force_ocr=True, image_dpi=300)

            # Open the OCR-enhanced PDF for text extraction
            with open(output_pdf_path, 'rb') as output_pdf:
                output_img = pdf2image.convert_from_bytes(output_pdf.read())
                text = pytesseract.image_to_string(output_img[0], lang='eng')

            # Clean up temporary files
            os.remove(img_path)
            os.remove(output_pdf_path)

        logging.info(f"Extracted text from {pdf_path}")
        print(f"Extracted text from {pdf_path}.")
        return text
    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {e}")
        print(f"Error processing {pdf_path}: {e}")
        return None

def classify_paper(text, client):
    if not text:
        logging.info("No text found for classification.")
        print("No text found for classification.")
        return "unknown"
    prompt = f"Based on the following abstract from a research paper, determine if the content is focused on biological life sciences. Respond with only one word, 'yes' for biological life sciences and 'no' for other fields. Abstract: {text}"
    try:
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip().lower()
        logging.info(f"Prompt to LLM: {prompt}")
        logging.info(f"LLM response: {result}")
        print(f"Sent prompt to LLM: {prompt}")
        print(f"LLM response: {result}")
        return result
    except Exception as e:
        logging.error(f"Error during classification: {e}")
        print(f"Error during classification: {e}")
        return "unknown"

def process_file(pdf_path, input_dir, output_dir, client):
    text = extract_text_from_first_page(pdf_path)
    classification = classify_paper(text, client)
    if classification == "no":
        try:
            shutil.move(pdf_path, os.path.join(output_dir, os.path.basename(pdf_path)))
            logging.info(f"Moved {os.path.basename(pdf_path)} to non-life sciences directory.")
            print(f"Moved {os.path.basename(pdf_path)} to non-life sciences directory.")
        except Exception as e:
            logging.error(f"Error moving {os.path.basename(pdf_path)}: {e}")
            print(f"Error moving {os.path.basename(pdf_path)}: {e}")

def move_non_life_sciences_pdfs(input_dir, output_dir, client):
    file_count = 0
    total_files = len([name for name in os.listdir(input_dir) if name.lower().endswith('.pdf')])
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            process_file(pdf_path, input_dir, output_dir, client)
            file_count += 1
            if file_count % 10 == 0:
                logging.info(f"Processed {file_count} files out of {total_files}, pausing for 10 minutes...")
                print(f"Processed {file_count} files out of {total_files}, pausing for 10 minutes...")
                time.sleep(120)  # Pause for 2 minutes for testing, change to 600 for 10 minutes in production
    logging.info(f"All {file_count} files processed.")
    print(f"All {file_count} files processed.")

# Initialize the client for your LLM
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Directory paths
input_dir = "D:\\Extracted_Research_Papers\\10.1002"
output_dir = "D:\\NonLifeSci_Papers\\10.1002"


move_non_life_sciences_pdfs(input_dir, output_dir, client)
