import os
import json
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

def main():
    directory = "."
    cv_data = {}
    
    print("Scanning for PDF files...")
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            print(f"Processing: {filename}")
            file_path = os.path.join(directory, filename)
            text = extract_text_from_pdf(file_path)
            cv_data[filename] = text
            
    # Save to a JSON file for easy reading by the agent
    with open("extracted_cvs.json", "w", encoding="utf-8") as f:
        json.dump(cv_data, f, indent=4, ensure_ascii=False)
    
    print(f"Extraction complete. Processed {len(cv_data)} files.")
    print("Saved to extracted_cvs.json")

if __name__ == "__main__":
    main()
