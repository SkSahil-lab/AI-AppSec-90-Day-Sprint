import time
def security_schema_gaurd(input_json_payload):
    start_time=time.perf_counter()
    allowed_keys = ["user_prompt", "session_id"]
    for key in input_json_payload.keys():
        if key not in allowed_keys:
         print(f"Security Breach : Unauthorized json input\n")
         return False

    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    print(f"TELEMETRY: Schema validation completed in {latency_ms:.4f} ms\n")
    return True

print("--- Launching Layer 3 Schema Firewall ---\n")
clean_payload = {
    "user_prompt": "Tell me how an API works.",
    "session_id": "90_DAY_SPRINT_USER_01"
}
print("📋 Testing System with Clean Structured Payload...")
security_schema_gaurd(clean_payload)

malicious_payload = {
    "user_prompt": "Tell me how an API works.",
    "session_id": "90_DAY_SPRINT_USER_01",
    "is_admin_override": True  #Hidden attack vector key!
}
print("📋 Testing System with Malicious Structural Payload...")
security_schema_gaurd(malicious_payload)
