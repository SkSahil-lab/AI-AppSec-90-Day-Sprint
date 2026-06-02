# Day 6: Modular Prompt Validation Engine
def sanitize_and_inspect(data_packet):
    try:
        # Core Abstraction: Attempt to traverse the path to extract the raw prompt string
        user_prompt = data_packet["prompt"]
        
        # Security validation check
        if "jailbreak" in user_prompt.lower():
            return "🚨 STATE: MALICIOUS. Dangerous prompt signature intercepted."
        return f"🟢 STATE: SAFE. Forwarding prompt to LLM -> {user_prompt}"
        
    except KeyError:
        # Systemic Fail-Closed: Trap the exact missing property error to prevent an app crash
        return "⚠️ STATE: REJECTED. Missing mandatory 'prompt' data parameter key."

# --- SIMULATED WEB TRAFFIC TESTING ---
print(sanitize_and_inspect({"user": "Shaik", "prompt": "How do I secure an API?"}))
print(sanitize_and_inspect({"user": "Attacker", "intent": "malicious"})) # Missing 'prompt' key!