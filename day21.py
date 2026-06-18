import time
import json

def payload_volume_throttler(raw_input_text, max_char_limit=500, max_bytes_limit=1024):
    start_time = time.perf_counter()
    char_count = len(raw_input_text)
    if char_count > max_char_limit:
        return trigger_volume_alert(
            "PAYLOAD_CHARACTER_OVERFLOW", 
            f"Input length of {char_count} characters exceeded ceiling of {max_char_limit}.",
            start_time
        )    
    byte_footprint = len(raw_input_text.encode('utf-8'))
    if byte_footprint > max_bytes_limit:
        return trigger_volume_alert(
            "PAYLOAD_BYTE_OVERFLOW",
            f"Input size of {byte_footprint} bytes exceeded maximum capacity of {max_bytes_limit} bytes.",
            start_time
        )
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    return {
        "status": "PASSED",
        "volume_metrics": {
            "characters_analyzed": char_count,
            "bytes_analyzed": byte_footprint,
            "throttler_overhead_ms": round(latency_ms, 4)
        }
    }

def trigger_volume_alert(violation_type, details, start_time):
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    
    incident_log = {
        "layer": "payload_volume_throttler",
        "status": "DROPPED",
        "violation": violation_type,
        "evidence": details,
        "mitigation_latency_ms": round(latency_ms, 4)
    }
    print(json.dumps(incident_log))
    return {"status": "REJECTED", "error": violation_type}

if __name__ == "__main__":
    print("--- Launching Layer 5 Content Throttler Sandbox ---\n")
    
    clean_prompt = "Hello AI, can you summarize my code profile?"
    print(" Testing Clean Prompt Input...")
    print(f"Result: {payload_volume_throttler(clean_prompt)}\n")
    
    malicious_overflow_prompt = "A" * 600  # Generates 600 characters instantly
    print(" Testing Malicious Volumetric Overflow Attack...")
    print(f"Result: {payload_volume_throttler(malicious_overflow_prompt)}\n")