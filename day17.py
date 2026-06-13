import json
import time
import unicodedata

def security_unicode_sanitizer(user_input_text):
    start_time=time.perf_counter()
    hidden_chars=["\u200b", "\u200c", "\u200d", "\ufeff", "\u202e"]
    sanitized_text=user_input_text
    for char in hidden_chars:
        if char in sanitized_text:
            sanitized_text=sanitized_text.replace(char,"")
    normalized_text=unicodedata.normalize("NFKC" , sanitized_text)
    was_obfuscated=(user_input_text!=normalized_text)
    end_time=time.perf_counter()
    latency_ms=(end_time-start_time)*1000
    if was_obfuscated:
        print(json.dumps({"layer": "unicode_gate", "status": "CLEANSED", "action": "strip_hidden_bytes", "overhead_ms": round(latency_ms, 4)}))
        print(f"SECURITY NOTICE: Hidden text anomalies detected and neutralized.\n")
    return normalized_text

print("--- Launching Layer 7 Unicode Sanitizer Gate ---\n")

poisoned_payload = "sys\u200btem ov\u200berride"
print(" Testing Payload A (Hidden Zero-Width Token Poisoning)...")
print(f"Raw Input Visualized: {poisoned_payload}")

cleansed_output = security_unicode_sanitizer(poisoned_payload)
print(f"Purified Output Result: {cleansed_output}\n")
print("-" * 50 + "\n")

clean_payload = "Tell me a short story about an engineer."
print("Testing Payload B (Standard Legitimate Clean Traffic)...")
print(f"Raw Input Visualized: {clean_payload}")

safe_output = security_unicode_sanitizer(clean_payload)
print(f"Purified Output Result: {safe_output}\n")

