import json
import time
session_cache={}
def security_rate_limit_gate(user_id , max_requests=3 , time_window_secs=10):
    start_time=time.perf_counter()
    current_timestamp=time.time()
    if user_id not in session_cache:
        session_cache[user_id]=[]
    request_history=session_cache[user_id]
    eviction_threshold=current_timestamp-time_window_secs
    purged_history=[ts for ts in request_history if ts > eviction_threshold]
    session_cache[user_id]=purged_history
    if len(purged_history)>=max_requests:
        return trigger_alert("RATE_LIMIT_EXCEEDED", f"User session '{user_id}' triggered...",start_time)
    session_cache[user_id].append(current_timestamp)
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    return {
        "status": "PASSED",
        "rate_metrics": {
            "current_window_volume": len(session_cache[user_id]),
            "max_window_ceiling": max_requests,
            "overhead_ms": round(latency_ms, 4)}
    }
def trigger_alert(voilation_type , description , start_time):
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    log_alert={
        "layer": "rate_limiting_gate",
        "status": "BLOCKED",
        "violation": voilation_type,
        "details": description,
        "overhead_ms": round(latency_ms, 4)}
    print(json.dumps(log_alert))
    print(f"SECURITY NOTICE: {voilation_type} intercepted and contained.\n")
    return {"status": "REJECTED", "error": voilation_type}

if __name__ == "__main__":
    print("--- Launching Layer 4 Rate-Limiting Gate Interceptor ---\n")
    mock_attacker_id = "user_dev_sec_hacker_99"
    print(f" Testing Exploit Scenario (Automated Loop Attack from {mock_attacker_id})")
    for i in range(4):
        print(f"Request #{i+1} sent")
        result = security_rate_limit_gate(mock_attacker_id, max_requests=3, time_window_secs=5)
        if result["status"] == "PASSED":
            print(f"Clearance Result: {json.dumps(result)}\n")




