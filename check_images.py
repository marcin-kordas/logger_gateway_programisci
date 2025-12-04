import json
import os

def check_images():
    with open('data/candidates.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"CWD: {os.getcwd()}")
    
    for cand in data:
        name = cand['name']
        image_filename = name.replace(" ", "_") + ".png"
        
        paths = [
            os.path.join("images", image_filename),
            os.path.join("app", "images", image_filename),
            image_filename
        ]
        
        found = False
        for p in paths:
            if os.path.exists(p):
                print(f"[OK] Found image for {name} at {p}")
                found = True
                break
        
        if not found:
            print(f"[MISSING] Image for {name} not found. Looked in: {paths}")

if __name__ == "__main__":
    check_images()
