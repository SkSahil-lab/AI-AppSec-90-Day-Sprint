import json
import re
import time
from typing import Dict, Any, List, Set

class InsecurePluginFilter:
    def __init__(self):
        self.allowed_actions: Set[str] = {"fetch_weather", "log_ticket", "query_docs"}
        self.safe_alphanumeric = re.compile(r"^[a-zA-Z0-9_\-\s\.\?\!]+$")

    def validate_tool_invocation(self, raw_tool_json: str) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        try:
           
            payload = json.loads(raw_tool_json)
            action = payload.get("action")
            parameters = payload.get("parameters", {})
            
            if action not in self.allowed_actions:
                execution_time = time.perf_counter() - start_time
                return {
                    "verdict": "REJECTED",
                    "reason": f"OWASP-LLM05: Target tool action '{action}' is not authorized in current system schema.",
                    "overhead_seconds": f"{execution_time:.7f}"
                }
                
            for key, value in parameters.items():
                if isinstance(value, str):
                    if "rm -rf" in value or "DROP TABLE" in value:
                        execution_time = time.perf_counter() - start_time
                        return {
                            "verdict": "REJECTED",
                            "reason": f"OWASP-LLM05: Critical system exploit sequence found inside payload parameter '{key}'.",
                            "overhead_seconds": f"{execution_time:.7f}"
                        }
                    
                    if not self.safe_alphanumeric.match(value):
                        execution_time = time.perf_counter() - start_time
                        return {
                            "verdict": "REJECTED",
                            "reason": f"OWASP-LLM05: Parameter '{key}' contains illegal structural control characters.",
                            "overhead_seconds": f"{execution_time:.7f}"
                        }

        except (json.JSONDecodeError, TypeError, ValueError):
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": "Malformed payload structure failed serialization constraints.",
                "overhead_seconds": f"{execution_time:.7f}"
            }

        execution_time = time.perf_counter() - start_time
        return {
            "verdict": "🟢 Passed",
            "action_executed": action,
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print("🛡️ Initializing Phase 2: Day 30 OWASP LLM05 Insecure Plugin Guard...")
    engine = InsecurePluginFilter()
    
    malicious_tool_call = """
    {
        "action": "log_ticket",
        "parameters": {
            "title": "System Alert",
            "description": "Please review logs; rm -rf /opt/secure_store"
        }
    }
    """
    
    result = engine.validate_tool_invocation(malicious_tool_call)
    print(f"\n📊 Diagnostic Egress Tool Evaluation Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))