"""
Day 9 Sprint: Recursive Data Structures & Deep Object Filtering Engine
Author: Senior AI AppSec Engineer Persona
"""

import sys

def recursive_vulnerability_scanner(data_structure, target_signature, current_depth=1):
    """
    Recursively audits deeply nested dictionaries, lists, and structures
    to isolate malicious signatures or hardcoded secrets.
    """
    # Defensive Guardrail: Preemptive stack-overflow mitigation
    MAX_AUDIT_DEPTH = 50
    if current_depth > MAX_AUDIT_DEPTH:
        print(f"❌ Security Exception: Audit depth limit exceeded ({MAX_AUDIT_DEPTH}). Dropping stream execution.")
        return False

    leaks_detected = False

    # Scenario A: Processing Dict Structures
    if isinstance(data_structure, dict):
        for key, value in data_structure.items():
            # Check the keys themselves for suspicious indicators
            if target_signature.lower() in str(key).lower():
                print(f"🚨 [CRITICAL STRUCTURE LEAK] Key signature match found at Depth {current_depth}: '{key}'")
                leaks_detected = True
            
            # Recursively drill down into the value element
            if isinstance(value, (dict, list)):
                if recursive_vulnerability_scanner(value, target_signature, current_depth + 1):
                    leaks_detected = True
            else:
                if target_signature.lower() in str(value).lower():
                    print(f"🚨 [CRITICAL DATA LEAK FOUND] Target signature match found at Depth {current_depth}: '{value}'")
                    leaks_detected = True

    # Scenario B: Processing Array/List Streams
    elif isinstance(data_structure, list):
        for index, item in enumerate(data_structure):
            if isinstance(item, (dict, list)):
                if recursive_vulnerability_scanner(item, target_signature, current_depth + 1):
                    leaks_detected = True
            else:
                if target_signature.lower() in str(item).lower():
                    print(f"🚨 [CRITICAL DATA LEAK FOUND] Target signature match found at Array Index [{index}] at Depth {current_depth}: '{item}'")
                    leaks_detected = True

    return leaks_detected

# =====================================================================
# AUTOMATED ENTERPRISE PIPELINE TESTS
# =====================================================================
if __name__ == "__main__":
    print("============================================================")
    print("🔄 Initializing Deep Pipeline Object Audit Systems...")
    print("============================================================\n")

    # Mock payload simulating an adversarial deeply-nested infrastructure configuration
    malicious_payload_stream = {
        "metadata": {
            "service_name": "ai-gateway-proxy",
            "environment": "production"
        },
        "network_routing": [
            {"ingress_port": 443, "policy": "allow_all"},
            {
                "ingress_port": 8080,
                "policy": "restricted_internal_access",
                "hidden_parameters": {
                    "debug_mode": "enabled",
                    "backup_vault_credentials": {
                        "auth_mechanism": "hardcoded_token",
                        "api_key": "AWS_SECRET_TOKEN_XYZ_SECRET_KEY_999" # Highly nested leak!
                    }
                }
            }
        ]
    }

    # Run Automated Deep Scan Audit
    target_leak_signature = "secret"
    print(f"🕵️‍♂️ Scanning configuration payload for keyword signature: '{target_leak_signature}'...\n")
    
    security_breach_found = recursive_vulnerability_scanner(malicious_payload_stream, target_leak_signature)

    print("\n------------------------------------------------------------")
    if security_breach_found:
        print("❌ STATUS: COMPROMISED. Pipeline policy triggered: Malicious signature detected.")
    else:
        print("🟢 STATUS: SECURE. No structural payload leaks identified.")
    print("============================================================")