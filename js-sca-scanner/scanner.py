import json
import sys
import os # <-- Make sure you have imported the 'os' library

print("--- Running Custom JavaScript SCA Scanner ---")

# --- THIS IS THE FIX ---
# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build the full, reliable path to the vulnerability_db.json file
db_path = os.path.join(script_dir, 'vulnerability-db.json')
# --- END OF FIX ---

# The path to the package.json is relative to the project root, which is correct
# package_json_path = './vulnerable-react-app/package.json'
# Build the path relative to the script's location
package_json_path = os.path.join(os.path.dirname(script_dir), 'vulnerable-react-app', 'package.json')
try:
    # Use the new, robust path to open the database file
    with open(db_path, 'r') as f:
        vulnerability_db = json.load(f)
except FileNotFoundError:
    # This error message now shows the path we tried, which is great for debugging
    print(f"Error: Could not find vulnerability database at {db_path}")
    sys.exit(1)

all_findings = []
try:
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find {package_json_path}")
    sys.exit(1)

# --- Scanning Logic for package.json ---
dependencies = package_data.get('dependencies', {})
devDependencies = package_data.get('devDependencies', {})
all_dependencies = {**dependencies, **devDependencies}

for package, version in all_dependencies.items():
    clean_version = version.lstrip('^~')
    
    if package in vulnerability_db and clean_version in vulnerability_db[package]:
        vuln = vulnerability_db[package][clean_version]
        finding = {
            "id": vuln['id'],
            "message": vuln['description'],
            "package": f"{package}@{version}",
            "severity": vuln['severity']
        }
        all_findings.append(finding)

# --- Reporting Block ---
if not all_findings:
    print("✅ No vulnerable JavaScript dependencies found.")
    sys.exit(0)
else:
    print(f"🚨 Found {len(all_findings)} vulnerable JavaScript dependencies:")
    high_severity_found = False
    for finding in all_findings:
        print(f"  - [{finding['severity']}] {finding['package']}: {finding['message']}")
        if finding['severity'] in ['CRITICAL', 'HIGH']:
            high_severity_found = True

    if high_severity_found:
        print("\n🔥 Build FAILED due to HIGH or CRITICAL severity issues.")
        sys.exit(1)
    else:
        print("\n✅ Build PASSED with only LOW or MEDIUM severity issues.")
        sys.exit(0)