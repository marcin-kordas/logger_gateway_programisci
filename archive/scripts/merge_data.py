import json

# Existing data (simulated read from file for the script)
try:
    with open("candidates.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = []

# New data provided by user
new_info = [
  {
    "name": "Ihor Horalevych",
    "avail_from": "immediately",
    "expected_net": None,
    "exp_similar": "No",
    "skills_list": [
      "automation",
      "PLC",
      "industrial electronics",
      "project design",
      "SCADA",
      "C",
      "Embedded",
      "Linux",
      "microcontrollers",
      "assembly",
      "PCB design",
      "telemetry",
      "TCP/IP"
    ],
    "skills_optional": [
      "STM32",
      "FPGA",
      "EPLAN",
      "TIA Portal",
      "Automation Studio",
      "pneumatics",
      "hydraulics"
    ],
    "energy_experience": True,
    "OZE_experience": False,
    "EMS_experience": False,
    "modbus": False,
    "linux": True,
    "posix": False,
    "c_language": True,
    "multithreading": False,
    "tcp_ip": True,
    "git": False,
    "gdb": False,
    "gcc": False,
    "pv_experience": False,
    "storage_experience": False,
    "hardware_integration": True,
    "inverters": False,
    "batteries": False,
    "familiar_with_sector": True,
    "other": [
      "SEP up to 1kV",
      "Languages: Polish (fluent), Ukrainian, Russian, English (B1)",
      "driving license B"
    ],
    "comment": "Very extensive automation and hardware integration experience, less emphasis on OZE or PV. No explicit Modbus/EMS in CV, but has SCADA and PLC."
  },
  {
    "name": "Magdalena Nowakowska",
    "avail_from": "2025-11-20",
    "expected_net": 15000,
    "exp_similar": "Yes, >1 year",
    "skills_list": [
      "C",
      "Linux",
      "POSIX/pthreads",
      "Multithreading",
      "WebSockets",
      "PHP",
      "Delphi",
      "SQL",
      "project management"
    ],
    "skills_optional": [
      "MS SQL",
      "API",
      "pyCUDA",
      "PostgreSQL",
      "Firebird",
      "UML",
      "GIT",
      "SVN"
    ],
    "energy_experience": False,
    "OZE_experience": False,
    "EMS_experience": False,
    "modbus": False,
    "linux": True,
    "posix": True,
    "c_language": True,
    "multithreading": True,
    "tcp_ip": True,
    "git": True,
    "gdb": False,
    "gcc": False,
    "pv_experience": False,
    "storage_experience": False,
    "hardware_integration": False,
    "inverters": False,
    "batteries": False,
    "familiar_with_sector": False,
    "other": [
      "Project manager, analytic background, some business app focus"
    ],
    "comment": "Strong system programming, Linux, and C/POSIX background; no explicit energy or Modbus/OZE/EMS experience."
  },
  {
    "name": "Dawid Łukasik",
    "avail_from": "immediately",
    "expected_net": None,
    "exp_similar": False,
    "skills_list": [
      "electrical installation",
      "maintenance",
      "technical support",
      "IT support"
    ],
    "skills_optional": [],
    "energy_experience": False,
    "OZE_experience": False,
    "EMS_experience": False,
    "modbus": False,
    "linux": False,
    "posix": False,
    "c_language": False,
    "multithreading": False,
    "tcp_ip": False,
    "git": False,
    "gdb": False,
    "gcc": False,
    "pv_experience": False,
    "storage_experience": False,
    "hardware_integration": True,
    "inverters": False,
    "batteries": False,
    "familiar_with_sector": False,
    "other": [
      "Electrician support, basic IT"
    ],
    "comment": "No C, Linux, or programming/system skills relevant for the posting."
  },
  {
    "name": "Jakub Sobczuk",
    "avail_from": "immediately",
    "expected_net": 5000,
    "exp_similar": "Yes, <1 year",
    "skills_list": [
      "C",
      "Linux",
      "Java",
      ".NET",
      "Python",
      "JavaScript",
      "React",
      "OpenGL",
      "server admin",
      "network infrastructure"
    ],
    "skills_optional": [
      "Selenium"
    ],
    "energy_experience": False,
    "OZE_experience": False,
    "EMS_experience": False,
    "modbus": False,
    "linux": True,
    "posix": False,
    "c_language": True,
    "multithreading": False,
    "tcp_ip": False,
    "git": False,
    "gdb": False,
    "gcc": False,
    "pv_experience": False,
    "storage_experience": False,
    "hardware_integration": False,
    "inverters": False,
    "batteries": False,
    "familiar_with_sector": False,
    "other": [
      "Student, some C work in university projects, mainly full stack/admin"
    ],
    "comment": "Basic programming and Linux, but not senior/industry relevant for advanced OZE/EMS position."
  },
  {
    "name": "Artur Piskorski",
    "avail_from": "~30 days",
    "expected_net": None,
    "exp_similar": "Yes, >1 year",
    "skills_list": [
      "C",
      "Python",
      "Linux",
      "Modbus RTU/TCP",
      "MQTT",
      "Embedded",
      "Node-RED",
      "ESP32",
      "RS-485",
      "system integration",
      "network automation",
      "PCB design"
    ],
    "skills_optional": [
      "AI LLM integration",
      "no-code/low-code automation",
      "cloud integration",
      "API design",
      "SQL",
      "FreeRTOS",
      "Armbian",
      "Debian"
    ],
    "energy_experience": True,
    "OZE_experience": True,
    "EMS_experience": True,
    "modbus": True,
    "linux": True,
    "posix": False,
    "c_language": True,
    "multithreading": False,
    "tcp_ip": True,
    "git": False,
    "gdb": False,
    "gcc": False,
    "pv_experience": True,
    "storage_experience": True,
    "hardware_integration": True,
    "inverters": True,
    "batteries": True,
    "familiar_with_sector": True,
    "other": [
      "Extensive hardware+software integration in OZE projects, strong IoT, free/open source stack, low-code."
    ],
    "comment": "Most closely matches advanced sectoral/Modbus/OZE/EMS needs in direct experience; some focus on open source/no-code stack."
  },
  {
    "name": "Kamil Godek",
    "avail_from": "immediately",
    "expected_net": None,
    "exp_similar": "No",
    "skills_list": [
      "C",
      "Python",
      "Embedded",
      "STM32",
      "PCB design",
      "TCP/IP",
      "hardware diagnostics",
      "SQL",
      "Linux basics"
    ],
    "skills_optional": [
      "G-Code",
      "AI/ML",
      "haptics",
      "OpenCV",
      "PyTorch",
      "CAD",
      "Git",
      "SVN"
    ],
    "energy_experience": False,
    "OZE_experience": False,
    "EMS_experience": False,
    "modbus": True,
    "linux": True,
    "posix": False,
    "c_language": True,
    "multithreading": False,
    "tcp_ip": True,
    "git": True,
    "gdb": False,
    "gcc": False,
    "pv_experience": False,
    "storage_experience": False,
    "hardware_integration": True,
    "inverters": False,
    "batteries": False,
    "familiar_with_sector": False,
    "other": [
      "Strong embedded/PCB",
      "AI/ML orientation"
    ],
    "comment": "Strong C/Embedded/Modbus/TCP skillset; no explicit OZE/EMS or sector projects mentioned."
  },
  {
    "name": "Zuzanna Kot",
    "avail_from": "immediately",
    "expected_net": None,
    "exp_similar": False,
    "skills_list": [
      "C basics",
      "C++ basics",
      "Linux user",
      "MS Office",
      "math"
    ],
    "skills_optional": [
      "HTML",
      "CSS",
      "teaching/math tutoring"
    ],
    "energy_experience": False,
    "OZE_experience": False,
    "EMS_experience": False,
    "modbus": False,
    "linux": True,
    "posix": False,
    "c_language": True,
    "multithreading": False,
    "tcp_ip": False,
    "git": False,
    "gdb": False,
    "gcc": False,
    "pv_experience": False,
    "storage_experience": False,
    "hardware_integration": False,
    "inverters": False,
    "batteries": False,
    "familiar_with_sector": False,
    "other": [
      "Student, no practice yet"
    ],
    "comment": "Entry-level only. No relevant experience or advanced programming/system skills."
  }
]

# Merge logic
merged_data = []
for existing in existing_data:
    match = next((item for item in new_info if item["name"] == existing["name"]), None)
    if match:
        # Merge match into existing, preferring match for new fields
        # Note: 'skills' in existing is a dict of scores. 'skills_list' in match is a list of strings.
        # We renamed 'skills' to 'skills_list' in new_info manually above to avoid conflict.
        
        # Update existing with all keys from match
        existing.update(match)
    merged_data.append(existing)

# Save back
with open("candidates.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4, ensure_ascii=False)

print("Merge complete.")
