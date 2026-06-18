import time
import json
def security_schema_validation_gate(raw_json_payload , expected_keys_schema):
    start_time=time.perf_counter()
    try:
        parsed_payload=json.loads(raw_json_payload)
    except json.JSONDecodeError:
        return trigger_schema_alert(
            "MALFORMED_JSON_SYNTAX",
            "The incoming request failed structural syntax parsing and is completely invalid.",
            start_time
        )
    for expected_key , expected_type in expected_keys_schema.items():
        if expected_key not in parsed_payload:
            return trigger_schema_alert(
                "MISSING_SCHEMA_PARAMETER",
                f"Required parameter key '{expected_key}' is completely missing from the request.",
                start_time
            )
    actual_value=parsed_payload[expected_key]
    if  not isinstance(actual_value , expected_type):
        return trigger_schema_alert(
            "INVALID_PARAMETER_TYPE",
                f"Parameter '{expected_key}' expected data type '{expected_type.__name__}', but received type '{type(actual_value).__name__}'.",
                start_time
        )
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    return {
         "status": "PASSED",
        "schema_metrics": {
         "parameters_verified": list(parsed_payload.keys()),
         "schema_overhead_ms": round(latency_ms, 4)}
    }
def trigger_schema_alert(violation_type , details , start_time):
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    incident_log = {
        "layer": "schema_validation_gate",
        "status": "REJECTED",
        "violation": violation_type,
        "details": details,
        "overhead_ms": round(latency_ms, 4)
    }
    print(json.dumps(incident_log))
    return {"status":"Blocked" , "error" :violation_type}
if __name__ == "__main__":
    APPROVED_SCHEMA_RULE = {
        "user_id": str,
        "prompt": str
    }
    
    clean_json_input = '{"user_id": "client_99", "prompt": "Analyze this format."}'
    print(security_schema_validation_gate(clean_json_input, APPROVED_SCHEMA_RULE))