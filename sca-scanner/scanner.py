import json
import sys

print("--- Running Custom SCA Scanner ---")
db = json.load(open('./sca-scanner/vulnerability_db.json'))
requirements_file = './app/requirements.txt'

findings = []
with open(requirements_file, 'r') as f:
    for line in f:
        package, version = line.strip().split('==')
        if package in db and version in db[package]:
            vuln = db[package][version]
            findings.append(f"  - [{vuln['severity']}] {vuln['id']} found in {package}=={version}. Description: {vuln['description']}")

if findings:
    print(f"🚨 Found {len(findings)} vulnerable dependencies:")
    for finding in findings:
        print(finding)
    sys.exit(1)
else:
    print("✅ No vulnerable dependencies found.")
    sys.exit(0)