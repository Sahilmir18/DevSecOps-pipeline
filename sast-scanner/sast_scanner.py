import os
import re
import json
import sys

def scan_file(filepath, rules):
    findings = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            for rule in rules:
                if re.search(rule['pattern'], line):
                    findings.append(f"  - [{rule['severity']}] {rule['name']} found in {filepath} at line {line_num}.")
    return findings

print("--- Running Custom SAST Scanner ---")
rules = json.load(open('./sast-scanner/rules.json'))
all_findings = []

# Scan the 'app' directory for Python files
for root, _, files in os.walk('./app'):
    for file in files:
        if file.endswith('.py'):
            all_findings.extend(scan_file(os.path.join(root, file), rules))

if all_findings:
    print(f"🚨 Found {len(all_findings)} SAST issues:")
    for finding in all_findings:
        print(finding)
    # CRITICAL STEP: Exit with a non-zero code to fail the GitHub Action
    sys.exit(1) 
else:
    print("✅ No SAST issues found.")
    sys.exit(0)