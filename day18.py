import json
import time

def security_schema_enforcer(raw_json_payload):
    
    start_time = time.perf_counter()
    EXPECTED_KEYS = {"jsonrpc", "method", "params", "id"}
    ALLOWED_METHODS = {"query_status", "fetch_logs", "execute_read"}
    
    try:
        data = json.loads(raw_json_payload)
        if not isinstance(data, dict):
            raise ValueError("Payload must be a valid JSON object structure.")
            
        current_keys = set(data.keys())
        if not current_keys.issubset(EXPECTED_KEYS) or "method" not in data or "params" not in data:
            return trigger_alert("STRUCTURAL_VIOLATION", "Unexpected keys or missing structural attributes.", start_time)
            
        requested_method = data["method"]
        if requested_method not in ALLOWED_METHODS:
            return trigger_alert("UNAUTHORIZED_FUNCTION", f"Attempted to execute forbidden method: {requested_method}", start_time)
            
        params = data["params"]
        if not isinstance(params, dict):
            return trigger_alert("MALFORMED_PARAMETERS", "Method parameters must be structured as a key-value dictionary.", start_time)
            
        if "request_id" in params:
            req_id = params["request_id"]
            if isinstance(req_id, (int, float)) and (req_id < 1 or req_id > 9999):
                return trigger_alert("PARAMETER_RANGE_VIOLATION", f"Parameter out of safe programmatic bounds: {req_id}", start_time)
    
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        return {
            "status": "PASSED",
            "sanitized_payload": data,
            "overhead_ms": round(latency_ms, 4)
        }
        
    except json.JSONDecodeError:
        return trigger_alert("MALFORMED_JSON", "Failed to parse string into valid JSON block structure.", start_time)
    except Exception as e:
        return trigger_alert("RUNTIME_EXCEPTION", str(e), start_time)

def trigger_alert(anomaly_type, description, start_time):
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    
    log_alert = {
        "layer": "schema_enforcement_gate",
        "status": "BLOCKED",
        "violation": anomaly_type,
        "details": description,
        "overhead_ms": round(latency_ms, 4)
    }
    print(json.dumps(log_alert))
    print(f" SECURITY NOTICE: {anomaly_type} intercepted and contained.\n")
    return {"status": "REJECTED", "error": anomaly_type}

if __name__ == "__main__":
    print("--- Launching Layer 6 Schema Enforcer Interceptor ---\n")

    exploit_payload_1 = '{"jsonrpc": "2.0", "method": "system_override", "params": {"user": "admin"}, "id": 1}'
    print(" Testing Exploit Payload A (Unauthorized Method Call Injection)...")
    security_schema_enforcer(exploit_payload_1)
    print("-" * 60 + "\n")

    exploit_payload_2 = '{"jsonrpc": "2.0", "method": "query_status", "params": {"request_id": 999999}, "id": 2}'
    print(" Testing Exploit Payload B (Out-of-Bounds Parameter Range Fuzzing)...")
    security_schema_enforcer(exploit_payload_2)
    print("-" * 60 + "\n")

    clean_payload = '{"jsonrpc": "2.0", "method": "query_status", "params": {"request_id": 450}, "id": 3}'
    print(" Testing Safe Payload C (Standard Valid Structured API Traffic)...")
    success_output = security_schema_enforcer(clean_payload)
    print(f"Gateway Clearance Result: {json.dumps(success_output, indent=2)}\n")