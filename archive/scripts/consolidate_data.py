import json
import re

def parse_availability(avail_str):
    if not avail_str:
        return "Unknown"
    avail_str = avail_str.lower()
    if "immediate" in avail_str or "natychmiast" in avail_str:
        return "Immediate"
    if "30 days" in avail_str or "month" in avail_str or "miesiąc" in avail_str:
        return "1 Month"
    if "date" in avail_str: # e.g. specific date
        return "Specific Date"
    return "Negotiable"

def parse_salary(salary):
    if salary is None:
        return None
    try:
        return int(salary)
    except:
        return None

def map_skills_to_structure(skills_list, skills_scores):
    # Standardized canonical skill tree
    structure = {
        "languages": {
            "c": {"present": False, "score": 0},
            "cpp": {"present": False, "score": 0},
            "python": {"present": False, "score": 0},
            "java": {"present": False, "score": 0},
            "javascript": {"present": False, "score": 0},
            "assembly": {"present": False, "score": 0}
        },
        "domains": {
            "embedded": {"present": False, "score": 0},
            "energy_oze": {"present": False, "score": 0},
            "web_backend": {"present": False, "score": 0},
            "automation_plc": {"present": False, "score": 0}
        },
        "protocols": {
            "modbus": False,
            "mqtt": False,
            "tcp_ip": False,
            "serial_rs485": False,
            "websockets": False
        },
        "infrastructure": {
            "linux": False,
            "rtos": False,
            "docker": False,
            "git": False,
            "ci_cd": False
        }
    }

    # Helper to check presence in list (case insensitive)
    sl_lower = [s.lower() for s in skills_list] if skills_list else []
    
    def has(term):
        return any(term in s for s in sl_lower)

    # Languages
    structure["languages"]["c"]["present"] = has("c") or has("c_programming") or skills_scores.get("C_Programming", 0) > 0
    structure["languages"]["c"]["score"] = skills_scores.get("C_Programming", 0)
    
    structure["languages"]["cpp"]["present"] = has("c++") or has("cpp")
    structure["languages"]["python"]["present"] = has("python")
    structure["languages"]["java"]["present"] = has("java")
    structure["languages"]["javascript"]["present"] = has("javascript") or has("react") or has("node")
    structure["languages"]["assembly"]["present"] = has("assembly") or has("assembler")

    # Domains
    structure["domains"]["embedded"]["present"] = has("embedded") or has("stm32") or has("esp32") or skills_scores.get("Embedded_Systems", 0) > 0
    structure["domains"]["embedded"]["score"] = skills_scores.get("Embedded_Systems", 0)
    
    structure["domains"]["energy_oze"]["present"] = has("energy") or has("oze") or has("pv") or skills_scores.get("Energy_Domain", 0) > 0
    structure["domains"]["energy_oze"]["score"] = skills_scores.get("Energy_Domain", 0)
    
    structure["domains"]["automation_plc"]["present"] = has("plc") or has("scada") or has("automation")

    # Protocols
    structure["protocols"]["modbus"] = has("modbus")
    structure["protocols"]["mqtt"] = has("mqtt")
    structure["protocols"]["tcp_ip"] = has("tcp") or has("ip") or has("sockets")
    structure["protocols"]["serial_rs485"] = has("rs-485") or has("serial") or has("uart")
    structure["protocols"]["websockets"] = has("websocket")

    # Infrastructure
    structure["infrastructure"]["linux"] = has("linux") or has("debian") or has("armbian")
    structure["infrastructure"]["rtos"] = has("rtos") or has("freertos")
    structure["infrastructure"]["git"] = has("git")

    return structure

def main():
    try:
        with open("candidates.json", "r", encoding="utf-8") as f:
            raw_candidates = json.load(f)
    except FileNotFoundError:
        print("candidates.json not found")
        return

    structured_data = []

    for c in raw_candidates:
        # 1. Personal & Logistics
        logistics = {
            "availability_status": parse_availability(c.get("avail_from")),
            "salary_request_pln_net": parse_salary(c.get("expected_net")),
            "location_preference": "Krakow/Remote" # Default assumption or parse from text if available
        }

        # 2. Technical Profile (Structured)
        tech_profile = map_skills_to_structure(c.get("skills_list", []), c.get("skills", {}))

        # 3. Assessment & Fit
        validation = c.get("validation_status", {})
        narrative = c.get("bigger_picture_narrative", {})
        
        assessment = {
            "alignment_rating": validation.get("alignment", "UNKNOWN"),
            "persona_type": narrative.get("persona", "Unknown"),
            "culture_fit_summary": narrative.get("culture_fit", ""),
            "risk_factors": c.get("gap_analysis_detailed", []) if isinstance(c.get("gap_analysis_detailed"), list) else [c.get("gap_analysis", "")]
        }

        # 4. Interview Prep
        interview = {
            "recommended_questions": c.get("interview_strategy", [])
        }

        # Consolidated Object
        consolidated = {
            "id": c["name"].lower().replace(" ", "_"),
            "display_name": c["name"],
            "logistics": logistics,
            "technical_profile": tech_profile,
            "assessment": assessment,
            "interview_prep": interview,
            "meta": {
                "source_status": c.get("status"),
                "original_comment": c.get("comment")
            }
        }
        
        structured_data.append(consolidated)

    # Save to new file
    with open("candidates_structured.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    print(f"Consolidated {len(structured_data)} candidates into candidates_structured.json")

if __name__ == "__main__":
    main()
