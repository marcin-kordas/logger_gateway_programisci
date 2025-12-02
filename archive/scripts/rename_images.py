import os
import shutil
import json

# Wczytaj mapowanie
with open("image_mapping.json", "r", encoding="utf-8") as f:
    mappings = json.load(f)

# Utwórz katalog dla obrazów
os.makedirs("images", exist_ok=True)

# Dla każdego kandydata - wybierz pierwszy plik (wszystkie są duplikatami)
processed_candidates = set()

for mapping in mappings:
    candidate = mapping["candidate"]
    old_name = mapping["old"]
    new_name = mapping["new"]
    
    # Jeśli już przetwarzaliśmy tego kandydata, pomiń
    if candidate in processed_candidates:
        continue
    
    # Skopiuj plik
    src = old_name
    dst = os.path.join("images", new_name)
    
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"✓ Skopiowano: {candidate}")
        print(f"  Do: images/{new_name}")
        processed_candidates.add(candidate)
    else:
        print(f"✗ Nie znaleziono: {src[:80]}...")

print(f"\nPrzetworzono {len(processed_candidates)} obrazów")
print(f"Katalog: images/")

# Wyświetl listę plików w katalogu images
if os.path.exists("images"):
    print("\nZawartość katalogu images/:")
    for f in os.listdir("images"):
        if f.endswith(".png"):
            size_mb = os.path.getsize(os.path.join("images", f)) / (1024 * 1024)
            print(f"  - {f} ({size_mb:.2f} MB)")
