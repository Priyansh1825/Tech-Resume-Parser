import os
import fitz  # PyMuPDF
import pandas as pd
import re
import pytesseract
from PIL import Image
from tqdm import tqdm

# --- WINDOWS TESSERACT PATH ---
# Make sure this matches the path you used in app.py!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# The exact path to your dataset
DATASET_PATH = r"D:\MY project\CV Dataset\Resumes PDF"
OUTPUT_CSV = "resume_dataset.csv"

def clean_text(text):
    """Removes weird characters, multiple spaces, and newlines to make the text AI-friendly."""
    if not text:
        return ""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[\n\t\r]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text_from_pdf(pdf_path):
    """Extracts text, using Tesseract OCR if the PDF is an image."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            extracted = page.get_text()
            if extracted and extracted.strip():
                text += extracted + " "
            else:
                # 🚨 OCR FALLBACK: If page is blank, read it as an image!
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img) + " "
        doc.close()
    except Exception as e:
        pass # Silently skip totally corrupted files
    return text

def build_dataset():
    print(f"🚀 Scanning for PDFs inside: {DATASET_PATH}")
    
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Error: Could not find the folder.")
        return

    # 1. Deep Scan for PDFs
    all_pdf_paths = []
    for root, dirs, files in os.walk(DATASET_PATH):
        for file in files:
            if file.lower().endswith('.pdf'):
                all_pdf_paths.append(os.path.join(root, file))
                
    print(f"📂 Found {len(all_pdf_paths)} PDF files. Starting extraction...\n")

    dataset = []
    
    # 2. Extract text with progress bar
    for pdf_path in tqdm(all_pdf_paths, desc="Processing Resumes"):
        job_role = os.path.basename(os.path.dirname(pdf_path))
        
        raw_text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(raw_text)
        
        # Now it will actually find text and save it!
        if cleaned_text:
            dataset.append({
                "Job_Role": job_role, 
                "Filename": os.path.basename(pdf_path),
                "Resume_Text": cleaned_text
            })

    # 3. Save to CSV
    if len(dataset) > 0:
        df = pd.DataFrame(dataset)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n✅ Extraction Complete! Successfully extracted {len(df)} resumes.")
        print(f"💾 Saved dataset to: {OUTPUT_CSV}")
    else:
        print("\n❌ Extraction Failed. Still found 0 text. Tesseract might not be configured correctly.")

if __name__ == "__main__":
    build_dataset()