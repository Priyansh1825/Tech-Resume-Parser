import os

# Let's test the exact path from your screenshot
DATASET_PATH = r"D:\MY project\CV Dataset\Resumes PDF"

print("--- DIRECTORY RADAR ---")
print(f"1. Does the folder exist at all? : {os.path.exists(DATASET_PATH)}")

if os.path.exists(DATASET_PATH):
    print("\n2. Looking inside the first few folders...")
    
    file_count = 0
    pdf_count = 0
    other_files = []
    
    # Do a quick scan
    for root, dirs, files in os.walk(DATASET_PATH):
        for file in files:
            file_count += 1
            if file.lower().endswith('.pdf'):
                pdf_count += 1
            else:
                other_files.append(file)
                
    print(f"\n📊 Total files found (of ANY type): {file_count}")
    print(f"📄 Total strict '.pdf' files found: {pdf_count}")
    
    if len(other_files) > 0:
        print(f"\n⚠️ WARNING: I found {len(other_files)} files that are NOT PDFs. Here are the first 5 examples:")
        for f in other_files[:5]:
            print(f"   - {f}")
            
print("-----------------------")