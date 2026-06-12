import json
import time
bucket_registery={}
def security_token_bucket(session_id , max_tokens=3):
    start_time=time.perf_counter()
    if session_id not in bucket_registery:
        bucket_registery[session_id]=max_tokens
    current_balance=bucket_registery[session_id]
    if current_balance <= 0:
         print(json.dumps({"layer": "token_bucket", "status": "DENIED", "session": session_id, "tokens_left": current_balance}))
         print(f"BURST LIMIT EXCEEDED: Session '{session_id}' has drained their token bucket balance. Request dropped.\n")
         return False
    bucket_registery[session_id]=current_balance-1
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    print(json.dumps({"layer": "token_bucket", "status": "AUTHORIZED", "session": session_id, "tokens_left": bucket_registery[session_id], "overhead_ms": round(latency_ms, 4)}))
    print(f"BURST PASS: Authorized prompt for '{session_id}'. Remaining tokens: {bucket_registery[session_id]}\n")
    return  True
print("--- Launching Layer 6 Token-Bucket Counter ---\n")
print(" Prompt 1 arriving rapidly...")
security_token_bucket("User_Burst_VIP")
print(" Prompt 2 arriving rapidly...")
security_token_bucket("User_Burst_VIP")
print(" Prompt 3 arriving rapidly...")
security_token_bucket("User_Burst_VIP")
print(" BUCKET DEPLOYED. ATTEMPTING INJECTION SPAM STRIKE...\n")
print(" Prompt 4 arriving instantly...")
security_token_bucket("User_Burst_VIP")

