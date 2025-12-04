import json
import os

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def transform_candidate(new_cand):
    name = new_cand.get('name')
    narrative = new_cand.get('bigger_picture_narrative', {})
    evidence = new_cand.get('external_evidence', {})
    tech_skills = evidence.get('technical_hard_skills', [])
    soft_skills = evidence.get('soft_skills_culture', [])
    
    # Default scores (will be overwritten by specific logic)
    scores = {
        "C_Programming": 5,
        "Embedded_Systems": 5,
        "Energy_Domain": 1,
        "Soft_Skills": 5,
        "Leadership_Experience": 3
    }
    
    status = "Review"
    expected_net = None
    exp_similar = "Nie"
    
    # Specific logic for known new candidates
    if "Arkadiusz Tyran" in name:
        scores = {
            "C_Programming": 9,
            "Embedded_Systems": 9,
            "Energy_Domain": 3,
            "Soft_Skills": 8,
            "Leadership_Experience": 7
        }
        status = "Recommended"
        expected_net = 20000 # Estimate based on range
        exp_similar = "Nie"
    elif "Mikita Khaladenka" in name:
        scores = {
            "C_Programming": 3,
            "Embedded_Systems": 2,
            "Energy_Domain": 1,
            "Soft_Skills": 6,
            "Leadership_Experience": 2
        }
        status = "Junior / Intern"
        expected_net = 0 # "staż za darmo" mentioned in user prompt
        exp_similar = "Nie"
    elif "Fryderyk Musiał" in name:
        scores = {
            "C_Programming": 8,
            "Embedded_Systems": 4,
            "Energy_Domain": 1,
            "Soft_Skills": 8,
            "Leadership_Experience": 5
        }
        status = "Consider for Senior Generalist"
        expected_net = 7000 # From user prompt
        exp_similar = "Tak, do roku" # From user prompt
        
    # Construct the new object matching candidates.json schema
    transformed = {
        "name": name,
        "skills": scores,
        "gap_analysis": new_cand.get('gap_analysis', []),
        "search_findings": str(new_cand.get('research_methodology', {}).get('verification_status', {}).get(name.replace(" ", "_"), "See detailed dossier")),
        "status": status,
        "avail_from": new_cand.get('additional_info', {}).get('avail_from', "Unknown"),
        "expected_net": expected_net,
        "exp_similar": exp_similar,
        "skills_list": tech_skills,
        "skills_optional": soft_skills,
        # Boolean flags - estimating based on skills list
        "energy_experience": False,
        "OZE_experience": False,
        "EMS_experience": False,
        "modbus": any("Modbus" in s for s in tech_skills),
        "linux": any("Linux" in s for s in tech_skills),
        "posix": any("POSIX" in s for s in tech_skills),
        "c_language": any("C" in s or "C++" in s for s in tech_skills),
        "multithreading": any("thread" in s.lower() for s in tech_skills),
        "tcp_ip": any("TCP" in s for s in tech_skills),
        "git": any("Git" in s for s in tech_skills),
        "gdb": False,
        "gcc": False,
        "pv_experience": False,
        "storage_experience": False,
        "hardware_integration": False,
        "inverters": False,
        "batteries": False,
        "familiar_with_sector": False,
        "other": [narrative.get('narrative', '')],
        "comment": narrative.get('culture_fit', ''),
        "validation_status": new_cand.get('validation_status', {}),
        "bigger_picture_narrative": narrative,
        "interview_strategy": new_cand.get('interview_strategy', []),
        "external_evidence": evidence,
        "gap_analysis_detailed": new_cand.get('gap_analysis', [])
    }
    
    # Refine booleans for Arkadiusz (Embedded expert)
    if "Arkadiusz Tyran" in name:
        transformed["hardware_integration"] = True
        transformed["multithreading"] = True # FreeRTOS
        
    return transformed

def main():
    existing_path = "data/candidates.json"
    new_path = "data/candidate_intelligence_dossiers_2_ENHANCED.json"
    
    existing_data = load_json(existing_path)
    new_data_full = load_json(new_path)
    new_candidates = new_data_full.get("candidate_intelligence_dossiers", [])
    
    # Create a set of existing names to avoid duplicates
    existing_names = {c['name'] for c in existing_data}
    
    added_count = 0
    for cand in new_candidates:
        if cand['name'] not in existing_names:
            print(f"Adding {cand['name']}...")
            transformed = transform_candidate(cand)
            existing_data.append(transformed)
            added_count += 1
        else:
            print(f"Skipping {cand['name']} (already exists)")
            
    if added_count > 0:
        save_json(existing_data, existing_path)
        print(f"Successfully added {added_count} candidates to {existing_path}")
    else:
        print("No new candidates added.")

if __name__ == "__main__":
    main()
