import time
import json
rate_limit_cache={}
def security_rate_limiter(session_id,rate_window_secs=10):
    start_time=time.perf_counter()
    current_time=time.time()
    if session_id in rate_limit_cache:
        last_request_time=rate_limit_cache[session_id]
        time_passed=current_time-last_request_time
        if time_passed < rate_window_secs:
            print(json.dumps({"layer": "rate_limiter", "status": "DENIED", "session": session_id, "cooldown_remains": round(rate_window_secs - time_passed, 2)}))
            print(f"RATE LIMIT EXCEEDED: User '{session_id}' must wait another {rate_window_secs - time_passed:.2f} seconds.\n")
            return False
    rate_limit_cache[session_id]=current_time
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000 
    print(json.dumps({"layer": "rate_limiter", "status": "AUTHORIZED", "session": session_id, "overhead_ms": round(latency_ms, 4)}))   
    print(f"RATE LIMIT PASS: Access authorized for session '{session_id}'.\n")
    return True
print("--- Launching Layer 5 Rate-Limiter Testing ---\n")
print("[0.5s] Request 2: User_Beta triggers an action...")
security_rate_limiter("User_Beta")
print("⌛ Waiting 11 seconds to let the cooldown window expire...")
time.sleep(11)
print("\n🚀 [12.0s] Request 4: User_Alpha returns after waiting patiently...")
security_rate_limiter("User_Alpha")