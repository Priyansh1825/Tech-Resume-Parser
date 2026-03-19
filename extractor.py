import pdfminer.high_level
import docx2txt
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    return pdfminer.high_level.extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    return docx2txt.process(docx_path)

def get_resume_text(file_path):
    """Identifies file type and calls the appropriate extractor."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format."

# Quick test (Make sure you have a sample file in data/raw/)
# if __name__ == "__main__":
#     text = get_resume_text('data/raw/sample_resume.pdf')
#     print(text)