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
                    # Use hcl2 to parse the Terraform file into a Python dictionary
                    terraform_code = hcl2.load(f)
                    
                    # Look through all defined resources in the file
                    for resource in terraform_code.get('resource', []):
                        for resource_type, resource_config in resource.items():
                            for resource_name, config_data in resource_config.items():
                                # Now, check this resource against our rules
                                for rule in rules:
                                    if rule['resource_type'] == resource_type:
                                        # Check for simple attributes first
                                        if rule['attribute'] in config_data and config_data[rule['attribute']] == rule['invalid_value']:
                                            finding = f"  - [{rule['severity']}] {rule['id']}: {rule['message']} (in resource '{resource_name}')"
                                            all_findings.append(finding)
                                        
                                        # Check for attributes inside nested blocks (like NSG security_rule)
                                        for block in config_data.get('security_rule', []):
                                            if rule['attribute'] in block and block[rule['attribute']] == rule['invalid_value']:
                                                finding = f"  - [{rule['severity']}] {rule['id']}: {rule['message']} (in resource '{resource_name}')"
                                                all_findings.append(finding)

                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")

if not tf_files_found:
    print("No Terraform files (.tf) found to scan.")

# --- Report the results ---
if all_findings:
    print(f"\n🚨 Found {len(all_findings)} IaC issues:")
    for finding in all_findings:
        print(finding)
    sys.exit(1) # Fail the pipeline
else:
    print("\n✅ No IaC issues found.")
    sys.exit(0) # Pass the pipeline