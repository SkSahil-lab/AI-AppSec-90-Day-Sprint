import time
import json

def security_type_length_gate(raw_user_input, max_bytes=1000, max_chars=500):
    """
    Layer 5 Security Gateway: Enforces data-type compliance and truncates/blocks
    volumetric string floods to protect the LLM context window from resource exhaustion.
    """
    start_time = time.perf_counter()
    
    # 1. Base Data-Type Validation
    if not isinstance(raw_user_input, str):
        actual_type = type(raw_user_input).__name__
        return trigger_alert(
            "INVALID_DATA_TYPE", 
            f"Expected string data type, received type: '{actual_type}'", 
            start_time
        )
        
    input_char_count = len(raw_user_input)
    input_byte_count = len(raw_user_input.encode('utf-8'))
    
    # 3. Volumetric Limit Threshold Checks
    if input_char_count > max_chars:
        return trigger_alert(
            "CHARACTER_LIMIT_EXCEEDED", 
            f"Input contains {input_char_count} characters. Maximum allowed is {max_chars}.", 
            start_time
        )
        
    if input_byte_count > max_bytes:
        return trigger_alert(
            "BYTE_SIZE_LIMIT_EXCEEDED", 
            f"Input footprint is {input_byte_count} bytes. Maximum allowed is {max_bytes}.", 
            start_time
        )
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    
    return {
        "status": "PASSED",
        "metrics": {
            "characters": input_char_count,
            "bytes": input_byte_count,
            "overhead_ms": round(latency_ms, 4)
        },
        "purified_data": raw_user_input
    }

def trigger_alert(violation_type, description, start_time):
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    
    log_alert = {
        "layer": "type_and_length_gate",
        "status": "BLOCKED",
        "violation": violation_type,
        "details": description,
        "overhead_ms": round(latency_ms, 4)
    }
    print(json.dumps(log_alert))
    print(f" SECURITY NOTICE: {violation_type} intercepted and contained.\n")
    return {"status": "REJECTED", "error": violation_type}


if __name__ == "__main__":
    print("--- Launching Layer 5 Type & Length Gate Interceptor ---\n")

    exploit_payload_1 = ["__override_admin_flag", "grant_access=True"]
    print(" Testing Exploit Payload A (Type Fuzzing Object Injection)...")
    security_type_length_gate(exploit_payload_1)
    print("-" * 60 + "\n")

    exploit_payload_2 = "A" * 2000  
    print(" Testing Exploit Payload B (Volumetric Content Length Flood)...")
    security_type_length_gate(exploit_payload_2)
    print("-" * 60 + "\n")

    clean_payload = "How do I secure my backend API endpoints?"
    print(" Testing Safe Payload C (Standard Legitimate User Request)...")
    success_output = security_type_length_gate(clean_payload)
    print(f"Gateway Clearance Result: {json.dumps(success_output, indent=2)}\n")