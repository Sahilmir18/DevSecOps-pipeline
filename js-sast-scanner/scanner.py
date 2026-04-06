# js-sast-scanner/scanner.py
import os
import re
import json
import sys

def scan_file(filepath, rules):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        for rule in rules:
            pattern = rule['pattern']
            try:
                regex = re.compile(pattern)
                for line_num, line in enumerate(lines, 1):
                    if regex.search(line):
                        finding = {
                            "id": rule['id'],
                            "message": rule['message'],
                            "file": filepath,
                            "line": line_num,
                            "severity": rule['severity']
                        }
                        findings.append(finding)
            except re.error:
                print(f"Invalid regex pattern in rule {rule['id']}: {pattern}")
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    
    return findings

print("--- Running Custom JavaScript SAST Scanner ---")

script_dir = os.path.dirname(os.path.abspath(__file__))
rules_path = os.path.join(script_dir, 'rules.json')
scan_directory = os.path.join(os.path.dirname(script_dir), 'vulnerable-react-app')

try:
    with open(rules_path, 'r') as f:
        rules = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find rules file at {rules_path}")
    sys.exit(1)

all_findings = []
for root, dirs, files in os.walk(scan_directory):
    # Skip node_modules directory
    dirs[:] = [d for d in dirs if d != 'node_modules']
    
    for file in files:
        if file.endswith('.js') or file.endswith('.jsx'):
            full_path = os.path.join(root, file)
            all_findings.extend(scan_file(full_path, rules))

if not all_findings:
    print("✅ No vulnerabilities found.")
    sys.exit(0)
else:
    print(f"🚨 Found {len(all_findings)} vulnerabilities:")
    high_severity_found = False
    for finding in all_findings:
        print(f"  - [{finding['severity']}] {finding['file']} (Line {finding['line']}): {finding['message']}")
        if finding['severity'] in ['CRITICAL', 'HIGH']:
            high_severity_found = True
    
    if high_severity_found:
        print("\n🔥 Build FAILED due to HIGH or CRITICAL severity issues.")
        sys.exit(1)
    else:
        print("\n✅ Build PASSED with only LOW or MEDIUM severity issues.")
        sys.exit(0)