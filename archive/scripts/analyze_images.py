import os
import json
import shutil

# Wczytaj listę kandydatów
with open("candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)

candidate_names = [c["name"] for c in candidates]
print("Kandydaci w bazie:")
for i, name in enumerate(candidate_names, 1):
    print(f"{i}. {name}")

# Znajdź wszystkie pliki PNG
png_files = [f for f in os.listdir(".") if f.endswith(".png")]
print(f"\n\nZnaleziono {len(png_files)} plików PNG:")
for i, f in enumerate(png_files, 1):
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f"{i}. {f[:100]}... ({size_mb:.2f} MB)")

# Wyświetl pełne nazwy
print("\n\nPełne nazwy plików PNG:")
for i, f in enumerate(png_files, 1):
    print(f"\n{i}. {f}")
