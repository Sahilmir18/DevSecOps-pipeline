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

# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build the full path to the rules.json file
rules_path = os.path.join(script_dir, 'rules.json')

print("--- Running Custom SAST Scanner ---") # REMOVED the duplicate print from before this line

try:
    # Use the new, reliable path to open the file
    with open(rules_path, 'r') as f:
        rules = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find rules file at {rules_path}")
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