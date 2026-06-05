"""
Day 10 Sprint: Input Length Validation Gate & Performance Latency Telemetry Engine
Author: AI Micro-SaaS Founder Persona
"""
import time

def security_gate_length(user_input_string, max_characters_allowed=1000):
    start_time = time.perf_counter()
    input_length = len(user_input_string)
    
    if input_length > max_characters_allowed:
        print(f"Security_alert : Max characters exceeded")
        is_secure = False
    else:
        print(f"Success :Characters allowed")
        is_secure = True
        
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    print(f"⏱️ TELEMETRY LOG: Guardrail execution took {latency_ms:.4f} ms\n")
    return is_secure

# 🌟 Crucial: Pushed all the way to the left margin!
print("--- Starting Live Perimeter Check ---")
security_gate_length("Hello world, this is my custom code execution!")
security_gate_length("ATTACK_VECTOR_PADDING_PADDING_" * 150)