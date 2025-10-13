# In sast-scanner/scanner.py

import os
import re
import json
import sys

# --- NEW DEBUGGING PRINTS ---
print("--- Starting Diagnostics ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"__file__ variable is: {__file__}")

script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Calculated script_dir: {script_dir}")

rules_path = os.path.join(script_dir, 'rules.json')
print(f"Calculated rules_path: {rules_path}")

print(f"Does rules_path exist? {os.path.exists(rules_path)}")
print("--- End Diagnostics ---")
# --- END DEBUGGING PRINTS ---

def scan_file(filepath, rules):
    # ... (rest of your function is the same)
    findings = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            for rule in rules:
                if re.search(rule['pattern'], line):
                    findings.append(f"  - [{rule['severity']}] {rule['name']} found in {filepath} at line {line_num}.")
    return findings

print("--- Running Custom SAST Scanner ---")

try:
    with open(rules_path, 'r') as f:
        rules = json.load(f)
except FileNotFoundError:
    print(f"CRITICAL ERROR: Could not find rules file at the calculated path: {rules_path}")
    sys.exit(1)



# Define the directory to scan
scan_directory = './app'
all_findings = []

# Scan the 'app' directory for Python files
# CHANGED to use the variable instead of a hardcoded path
for root, _, files in os.walk(scan_directory):
    for file in files:
        if file.endswith('.py'):
            # Build the full path for the file being scanned
            full_path = os.path.join(root, file)
            all_findings.extend(scan_file(full_path, rules))

if all_findings:
    print(f"🚨 Found {len(all_findings)} SAST issues:")
    for finding in all_findings:
        print(finding)
    # CRITICAL STEP: Exit with a non-zero code to fail the GitHub Action
    sys.exit(1) 
else:
    print("✅ No SAST issues found.")
    sys.exit(0)