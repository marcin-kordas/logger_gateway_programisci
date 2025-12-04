import pypdf
import os

files = [
    r"docs/cvs/CV_Fryderyk_Musiał_mgr_inz.pdf",
    r"docs/cvs/CV_Mikita_Khaladzenka.pdf",
    r"docs/cvs/CV - Arkadiusz Tyran ENG.pdf"
]

for f in files:
    print(f"--- START {os.path.basename(f)} ---")
    try:
        if not os.path.exists(f):
             print(f"File not found: {f}")
             continue
        reader = pypdf.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(text)
    except Exception as e:
        print(f"Error reading {f}: {e}")
    print(f"--- END {os.path.basename(f)} ---")
