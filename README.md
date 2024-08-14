# AI Research Paper Classification Agent

### Overview
This Python script automates the extraction of text from PDF documents, classifies the content using a locally hosted Language Model (LLM), and sorts the documents into directories based on whether they pertain to biological life sciences.

### Features
- **Text Extraction**: Extracts text from PDF files using PyMuPDF, with OCR fallback for PDFs that are difficult to read.
- **Classification**: Classifies PDF content to determine if it is related to biological life sciences using a local Language Model.
- **Automated Sorting**: Automatically moves non-life sciences PDFs to a separate directory for easier management.

### System Requirements
- **Python Version**: 3.6+
- **Operating System**: Compatible with Windows, macOS, and Linux.

### Dependencies
1. **PyMuPDF (fitz)**: For text extraction from PDF files.
   - **Installation**:
     ```bash
     pip install PyMuPDF
     ```

2. **ocrmypdf**: Adds an OCR text layer to PDFs, making them searchable.
   - **Installation**:
     ```bash
     pip install ocrmypdf
     ```

3. **Pytesseract**: Python wrapper for Google's Tesseract-OCR Engine.
   - **Installation**:
     ```bash
     pip install pytesseract
     ```
   - **Note**: Tesseract-OCR must be installed separately. [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract) has the installation instructions.

4. **pdf2image**: Converts PDF pages to images for OCR processing.
   - **Installation**:
     ```bash
     pip install pdf2image
     ```

5. **OpenAI Python Client**: Used to interact with the locally hosted LLM.
   - **Installation**:
     ```bash
     pip install openai
     ```

### Script Components

- **Logging Setup**: Sets up a logging system to track processing activities and errors.
- **Text Extraction**: Extracts text from the first page of PDFs using PyMuPDF or OCR as a fallback.
- **OCR Processing**: Converts PDF pages to images and extracts text using OCR.
- **Classification**: Sends extracted text to a local LLM for classification as life sciences or non-life sciences.
- **File Processing**: Sorts and moves PDFs to the appropriate directories based on classification results.

### How to Use

1. **Prepare Your Environment**:
   - Install the necessary dependencies listed above.
   - Ensure that the local LLM server is running.

2. **Set Directory Paths**:
   - Set the `input_dir` to the directory containing your PDF files.
   - Set the `output_dir` to the directory where non-life sciences PDFs should be moved.

3. **Run the Script**:
   - Execute the script to begin processing PDFs.
   - The script will extract text, classify each document, and move non-life sciences PDFs to the specified output directory.

### Example Execution
```python
from openai import OpenAI

client = OpenAI(api_key="your_openai_api_key")  # Replace with your API key
input_dir = "/path/to/your/input_directory"
output_dir = "/path/to/your/output_directory"

move_non_life_sciences_pdfs(input_dir, output_dir, client)
```

### License
This project is licensed under the MIT License.

### Contributions
Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes or enhancements.

---

This README provides a comprehensive overview of the script, its components, and how to use it. Adjust the paths and instructions as necessary to fit your specific environment and requirements.