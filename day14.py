import json
import time
def security_schema_gaurd(input_json_payload):
    allowed_keys=["user_prompt" , "session_id"]
    for key in input_json_payload.keys():
        if key not in allowed_keys:
            print(json.dumps({"layer": "schema" , "status": "Blocked" ,"trigger_key":key}))
            print(f"FORM ERROR: Unauthorized box label found -> '{key}'. Processing halted.\n")
            return False
    return True
def security_blacklist_filter(user_input_text):
    banned_tokens=["ignore previous instructions" , "system override"]
    clean_text=user_input_text.lower()
    for token in banned_tokens:
        if token in clean_text:
            print(json.dumps({"layer":"blacklist" , "status":"Blocked" , "trigger_tokens" :token}))
            print(f"THREAT DETECTED: A banned instruction phrase was intercepted. Request dropped. \n")
            return False
    return True
def prompt_firewall_orchestrator(input_api_payload):
    start_time=time.perf_counter()
    print("FIREWALL ACTIVE: Running security checks...\n")
    if not security_schema_gaurd(input_api_payload):
        return False
    user_text=input_api_payload.get("user_prompt","")
    if not security_blacklist_filter(user_text):
        return False
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    print(json.dumps({"pipeline": "complete", "status": "CLEARED", "overhead_ms": round(latency_ms, 4)}))
    print(f"SECURITY PASS: Request is safe. Forwarding to AI model.\n")
    return True

payload_a = {
    "user_prompt": "Hello! Write a 3-word sentence.",
    "session_id": "USER_771"
}
print("--- TEST A: Clean Data Flow ---")
prompt_firewall_orchestrator(payload_a)

