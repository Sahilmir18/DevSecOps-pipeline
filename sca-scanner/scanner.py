import json
import sys
import os # It's good practice to add this for the path fix

print("--- Running Custom SCA Scanner ---")

# --- Let's make these paths robust like we did for the SAST scanner ---
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'vulnerability_db.json')
requirements_file = './app/requirements.txt' # This path is fine as it's relative to the project root

try:
    with open(db_path, 'r') as f:
        db = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find vulnerability database at {db_path}")
    sys.exit(1)

findings = []
with open(requirements_file, 'r') as f:
    for line in f:
        # --- THIS IS THE FIX ---
        # 1. Strip whitespace from the line.
        # 2. Check if the line is not empty AND contains '=='.
        clean_line = line.strip()
        if clean_line and '==' in clean_line:
            # Now it's safe to split the line
            package, version = clean_line.split('==')
            
            if package in db and version in db[package]:
                vuln = db[package][version]
                findings.append(f"  - [{vuln['severity']}] {vuln['id']} found in {package}=={version}. Description: {vuln['description']}")
        # If the line is empty or doesn't have '==', the loop just continues to the next line.
        # --- END OF FIX ---

if findings:
    print(f"🚨 Found {len(findings)} vulnerable dependencies:")
    for finding in findings:
        print(finding)
    sys.exit(1)
else:
    print("✅ No vulnerable dependencies found.")
    sys.exit(0)