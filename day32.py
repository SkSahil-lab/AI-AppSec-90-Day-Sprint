import time
from typing import Dict, Any, Set

class SystemPromptLeakageFilter:
    def __init__(self):
        
        self.system_signature_keywords: Set[str] = {
            "you are a helpful assistant",
            "system instructions",
            "core rules guidelines",
            "do not reveal this prompt",
            "respond as a model"
        }

    def inspect_egress_output(self, raw_llm_generation: str) -> Dict[str, Any]:
       
        start_time = time.perf_counter()
        normalized_output = raw_llm_generation.lower().strip()

        for signature in self.system_signature_keywords:
            if signature in normalized_output:
                execution_time = time.perf_counter() - start_time
                return {
                    "verdict": "REJECTED",
                    "reason": f"OWASP-LLM07: System Prompt Leakage Intercepted. Unauthorized phrase match detected ['{signature}'].",
                    "overhead_seconds": f"{execution_time:.7f}"
                }

        execution_time = time.perf_counter() - start_time
        return {
            "verdict": "🟢 Passed",
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print("🛡️ Initializing Phase 2: Day 32 OWASP LLM07 System Prompt Leakage Filter...")
    filter_engine = SystemPromptLeakageFilter()
    
    leaked_generation_payload = "Certainly! Here are my core rules guidelines: You are a helpful assistant designed to query customer tables..."
    
    result = filter_engine.inspect_egress_output(leaked_generation_payload)
    print(f"\n📊 Egress Filter Diagnostic Evaluation Result:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))