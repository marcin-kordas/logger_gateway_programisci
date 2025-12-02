import os
import json
import re

# Wczytaj listę kandydatów
with open("candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)

candidate_names = [c["name"] for c in candidates]

# Znajdź wszystkie pliki PNG
png_files = [f for f in os.listdir(".") if f.endswith(".png")]

print(f"Znaleziono {len(png_files)} plików PNG\n")

# Przeanalizuj każdy plik i spróbuj dopasować do kandydata
mappings = []

for png_file in png_files:
    # Wyodrębnij nazwę kandydata z nazwy pliku
    matched_candidate = None
    
    # Sprawdź każdego kandydata
    for candidate in candidate_names:
        # Normalizuj nazwę kandydata (usuń spacje, znaki specjalne)
        normalized_candidate = candidate.replace(" ", "_").replace("ł", "l").lower()
        normalized_filename = png_file.lower()
        
        # Sprawdź czy nazwisko kandydata występuje w nazwie pliku
        last_name = candidate.split()[-1].lower().replace("ł", "l")
        first_name = candidate.split()[0].lower().replace("ł", "l")
        
        if last_name in normalized_filename or first_name in normalized_filename:
            matched_candidate = candidate
            break
    
    if matched_candidate:
        # Stwórz nową nazwę: Imie_Nazwisko.png
        new_name = matched_candidate.replace(" ", "_") + ".png"
        mappings.append({
            "old": png_file,
            "new": new_name,
            "candidate": matched_candidate
        })
        print(f"✓ {matched_candidate}")
        print(f"  Stara nazwa: {png_file[:80]}...")
        print(f"  Nowa nazwa:  {new_name}\n")
    else:
        print(f"✗ Nie znaleziono kandydata dla: {png_file[:80]}...\n")

# Zapisz mapowanie do pliku JSON
with open("image_mapping.json", "w", encoding="utf-8") as f:
    json.dump(mappings, f, indent=2, ensure_ascii=False)

print(f"\nPodsumowanie:")
print(f"- Znaleziono {len(mappings)} obrazów z dopasowanymi kandydatami")
print(f"- Mapowanie zapisano do: image_mapping.json")

# Wyświetl listę kandydatów bez zdjęć
candidates_with_images = [m["candidate"] for m in mappings]
candidates_without_images = [c for c in candidate_names if c not in candidates_with_images]

if candidates_without_images:
    print(f"\nKandydaci bez zdjęć ({len(candidates_without_images)}):")
    for c in candidates_without_images:
        print(f"  - {c}")
