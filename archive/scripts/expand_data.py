import json

# Read existing candidates
try:
    with open("candidates.json", "r", encoding="utf-8") as f:
        candidates = json.load(f)
except FileNotFoundError:
    print("candidates.json not found!")
    exit(1)

# Read dossiers
try:
    with open("candidate_intelligence_dossiers.json", "r", encoding="utf-8") as f:
        dossiers_data = json.load(f)
        dossiers = dossiers_data.get("candidate_intelligence_dossiers", [])
except FileNotFoundError:
    print("candidate_intelligence_dossiers.json not found!")
    exit(1)

# Merge logic
for cand in candidates:
    # Find matching dossier
    dossier = next((d for d in dossiers if d["name"] == cand["name"]), None)
    
    if dossier:
        # Fields to merge
        fields_to_merge = [
            "validation_status",
            "bigger_picture_narrative",
            "interview_strategy",
            "external_evidence" # This might overlap with skills, but good to have the structured text
        ]
        
        for field in fields_to_merge:
            if field in dossier:
                cand[field] = dossier[field]
        
        # Also update gap_analysis if the dossier version is better (it seems to be a list in dossier vs string in current)
        # Let's keep both or prefer dossier if it exists.
        # Current gap_analysis is a string. Dossier is a list.
        # Let's rename dossier's gap_analysis to 'gap_analysis_list' to avoid breaking existing string display, 
        # or join it.
        if "gap_analysis" in dossier and isinstance(dossier["gap_analysis"], list):
            cand["gap_analysis_detailed"] = dossier["gap_analysis"]

# Save back
with open("candidates.json", "w", encoding="utf-8") as f:
    json.dump(candidates, f, indent=4, ensure_ascii=False)

print("Expansion complete. Merged dossier data.")
