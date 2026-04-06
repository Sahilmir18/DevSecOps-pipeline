import os
import json
import sys
import hcl2 # The library for parsing Terraform files

print("--- Running Custom IaC Scanner for Terraform ---")

# --- Setup: Find files and load rules ---
script_dir = os.path.dirname(os.path.abspath(__file__))
rules_path = os.path.join(script_dir, 'rules.json')
scan_directory = './infrastructure'

try:
    with open(rules_path, 'r') as f:
        rules = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find rules file at {rules_path}")
    sys.exit(1)

# --- The Scanning Logic ---
all_findings = []
tf_files_found = False

for root, _, files in os.walk(scan_directory):
    for file in files:
        if file.endswith('.tf'):
            tf_files_found = True
            filepath = os.path.join(root, file)
            print(f"Scanning file: {filepath}")

            with open(filepath, 'r') as f:
                try:
                    terraform_code = hcl2.load(f)
                    
                    for resource in terraform_code.get('resource', []):
                        for resource_type, resource_config in resource.items():
                            for resource_name, config_data in resource_config.items():
                                for rule in rules:
                                    if rule['resource_type'] == resource_type:
                                        
                                        # CORRECTED: Create and append a dictionary for each finding
                                        def add_finding():
                                            finding = {
                                                "id": rule['id'],
                                                "message": rule['message'],
                                                "resource": resource_name,
                                                "severity": rule['severity']
                                            }
                                            all_findings.append(finding)

                                        # Check for simple attributes
                                        if rule['attribute'] in config_data and config_data[rule['attribute']] == rule['invalid_value']:
                                            add_finding()
                                        
                                        # Check for attributes inside nested blocks
                                        for block in config_data.get('security_rule', []):
                                            if rule['attribute'] in block and block[rule['attribute']] == rule['invalid_value']:
                                                add_finding()

                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")

if not tf_files_found:
    print("No Terraform files (.tf) found to scan.")

# --- Single, Correct Reporting Block with SEVERITY CHECK ---
if not all_findings:
    print("\n✅ No IaC issues found.")
    sys.exit(0)
else:
    print(f"\n🚨 Found {len(all_findings)} IaC issues:")
    high_severity_found = False
    for finding in all_findings:
        # Now this works because `finding` is a dictionary with a 'severity' key
        print(f"  - [{finding['severity']}] {finding['id']}: {finding['message']} (in resource '{finding['resource']}')")
        if finding['severity'] in ['CRITICAL', 'HIGH']:
            high_severity_found = True

    # ONLY fail the build if a critical or high issue was found
    if high_severity_found:
        print("\n🔥 Build FAILED due to HIGH or CRITICAL severity issues.")
        sys.exit(1)
    else:
        print("\n✅ Build PASSED with only LOW or MEDIUM severity issues.")
        sys.exit(0)