import json
import re
import time
from typing import Dict, Any, List, Set

class InsecurePluginFilter:
    def __init__(self):
        # Whitelist of explicitly authorized plugin integration actions
        self.allowed_actions: Set[str] = {"fetch_weather", "log_ticket", "query_docs"}
        # Strict alphanumeric pattern enforcement for basic string inputs
        self.safe_alphanumeric = re.compile(r"^[a-zA-Z0-9_\-\s\.\?\!]+$")

    def validate_tool_invocation(self, raw_tool_json: str) -> Dict[str, Any]:
        """
        Validates structure and schema constraints on outgoing model tool calls to prevent injection privilege escalation.
        """
        start_time = time.perf_counter()
        
        try:
            # Parse the tool call string into structured JSON map
            payload = json.loads(raw_tool_json)
            action = payload.get("action")
            parameters = payload.get("parameters", {})
            
            # Step 1: Strict action identifier whitelisting check
            if action not in self.allowed_actions:
                execution_time = time.perf_counter() - start_time
                return {
                    "verdict": "REJECTED",
                    "reason": f"OWASP-LLM05: Target tool action '{action}' is not authorized in current system schema.",
                    "overhead_seconds": f"{execution_time:.7f}"
                }
                
            # Step 2: Validate internal parameters against structural rules
            for key, value in parameters.items():
                if isinstance(value, str):
                    # Flag dangerous administrative shell operations
                    if "rm -rf" in value or "DROP TABLE" in value:
                        execution_time = time.perf_counter() - start_time
                        return {
                            "verdict": "REJECTED",
                            "reason": f"OWASP-LLM05: Critical system exploit sequence found inside payload parameter '{key}'.",
                            "overhead_seconds": f"{execution_time:.7f}"
                        }
                    
                    # Ensure parameters do not contain characters meant to breakout of execution blocks
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
    
    # Simulating a compromised tool request attempting shell breakthrough command strings
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