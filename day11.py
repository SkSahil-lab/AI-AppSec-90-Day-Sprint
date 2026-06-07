import time
def security_blacklist_filter(user_input_text):
    start_time = time.perf_counter()
    is_secure=True
    banned_tokens = ["ignore previous instructions", "system override", "read system prompt"]
    clean_text=user_input_text.lower()

    for token in banned_tokens:
        if token in clean_text:
            print(f"ALERT : The Banned Token --> '{token}'")
            is_secure = False
            break
    end_time = time.perf_counter()
    latency_ms=(end_time - start_time)* 1000
    print(f"The time taken for Latency --> '{latency_ms :.4f}'ms \n")
    return is_secure
print("--- Running the Security Blacklist Filter ---")
security_blacklist_filter('Hey there!')
security_blacklist_filter('system override')



