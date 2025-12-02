import json
import re

def parse_markdown_info(md_content):
    info_map = {}
    # Split by candidate sections
    sections = re.split(r'## \d+\. ', md_content)
    
    for section in sections:
        if not section.strip():
            continue
            
        # Extract name
        name_match = re.match(r'([^\(]+)', section)
        if not name_match:
            continue
        name = name_match.group(1).strip()
        
        info = {}
        
        # Extract availability
        avail_match = re.search(r'\*\*Kiedy możesz rozpocząć pracę\?\*\* (.+)', section)
        if avail_match:
            info['availability'] = avail_match.group(1).strip()
            
        # Extract experience
        exp_match = re.search(r'\*\*Czy masz doświadczenie w pracy na podobnym stanowisku\?\*\* (.+)', section)
        if exp_match:
            info['experience'] = exp_match.group(1).strip()
            
        # Extract salary
        sal_match = re.search(r'\*\*Jakie jest Twoje oczekiwane wynagrodzenie netto \(na rękę\)\?\*\* (.+)', section)
        if sal_match:
            info['salary'] = sal_match.group(1).strip()
            
        if info:
            info_map[name] = info
            
    return info_map

def normalize_name(name):
    return name.lower().replace("ł", "l").replace("david", "dawid").strip()

def parse_salary(salary_str):
    if not salary_str or salary_str == "-" or "brak" in salary_str.lower() or "do dogadania" in salary_str.lower():
        return None
    # Try to extract number
    nums = re.findall(r'\d+', salary_str.replace(" ", ""))
    if nums:
        return int(nums[0])
    return None

def main():
    # Read markdown
    try:
        with open("dodatkowe_info.md", "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        print("dodatkowe_info.md not found")
        return

    info_map = parse_markdown_info(md_content)
    print(f"Parsed info for {len(info_map)} candidates")

    # Update candidates.json
    try:
        with open("candidates.json", "r", encoding="utf-8") as f:
            candidates = json.load(f)
    except FileNotFoundError:
        print("candidates.json not found")
        return

    updated_count = 0
    for cand in candidates:
        cand_name_norm = normalize_name(cand["name"])
        
        # Try to find match
        matched_info = None
        for md_name, info in info_map.items():
            if normalize_name(md_name) == cand_name_norm:
                matched_info = info
                break
        
        if matched_info:
            # Update Availability
            if 'availability' in matched_info:
                cand["avail_from"] = matched_info['availability']
            
            # Update Experience
            if 'experience' in matched_info:
                cand["exp_similar"] = matched_info['experience']
                
            # Update Salary
            if 'salary' in matched_info:
                # Store raw string or parsed? candidates.json seems to have mixed or nulls. 
                # Let's try to store parsed number if possible, or null if not a number/range?
                # Actually, looking at file, expected_net is null or int.
                cand["expected_net"] = parse_salary(matched_info['salary'])

            updated_count += 1
            print(f"Updated {cand['name']}")

    with open("candidates.json", "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=4, ensure_ascii=False)
    
    print(f"Updated {updated_count} candidates in candidates.json")

    # Also try to update candidates_atomized_v2.json if it exists
    try:
        with open("candidates_atomized_v2.json", "r", encoding="utf-8") as f:
            candidates_v2_data = json.load(f)
            
        # Check structure
        if isinstance(candidates_v2_data, dict) and "candidates" in candidates_v2_data:
            candidates_list = candidates_v2_data["candidates"]
        elif isinstance(candidates_v2_data, list):
            candidates_list = candidates_v2_data
        else:
            print("Unknown structure for candidates_atomized_v2.json")
            return

        v2_updated_count = 0
        for cand in candidates_list:
            # Name might be in 'display_name' or 'name' or 'metadata.name'
            c_name = cand.get("name") or cand.get("display_name")
            if not c_name and "metadata" in cand:
                c_name = cand["metadata"].get("name")
            
            if not c_name:
                continue
                
            cand_name_norm = normalize_name(c_name)
            
            matched_info = None
            for md_name, info in info_map.items():
                if normalize_name(md_name) == cand_name_norm:
                    matched_info = info
                    break
            
            if matched_info:
                # Update Availability
                if 'availability' in matched_info:
                    if "availability" in cand and isinstance(cand["availability"], dict):
                        cand["availability"]["available_from_text"] = matched_info['availability']
                    elif "logistics" in cand and isinstance(cand["logistics"], dict):
                        cand["logistics"]["availability_status"] = matched_info['availability']
                    else:
                        cand["avail_from"] = matched_info['availability']
                
                # Update Salary
                if 'salary' in matched_info:
                    parsed_sal = parse_salary(matched_info['salary'])
                    if "availability" in cand and isinstance(cand["availability"], dict) and "salary" in cand["availability"]:
                         cand["availability"]["salary"]["expected_net_PLN"] = parsed_sal
                    elif "logistics" in cand and isinstance(cand["logistics"], dict):
                         cand["logistics"]["expected_salary"] = parsed_sal

                # Update Experience
                if 'experience' in matched_info:
                    exp_text = matched_info['experience']
                    has_exp = "tak" in exp_text.lower()
                    
                    if "experience" in cand and isinstance(cand["experience"], dict) and "similar_role" in cand["experience"]:
                        cand["experience"]["similar_role"]["detail"] = exp_text
                        cand["experience"]["similar_role"]["has_similar"] = has_exp
                        
                v2_updated_count += 1
        
        with open("candidates_atomized_v2.json", "w", encoding="utf-8") as f:
            json.dump(candidates_v2_data, f, indent=4, ensure_ascii=False)
        print(f"Updated {v2_updated_count} candidates in candidates_atomized_v2.json")
            
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Could not update candidates_atomized_v2.json: {e}")

if __name__ == "__main__":
    main()
