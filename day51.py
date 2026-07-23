import re
import time
import json
from typing import Dict, Any, List, Tuple

class DataLossPreventionEngine:
    def __init__(self):
        # High-precision regex pattern rulesets for common PII data types
        self.pii_patterns: Dict[str, str] = {
            "EMAIL_ADDRESS": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "US_SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "PHONE_NUMBER": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "IPV4_ADDRESS": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
            "API_KEY_GENERIC": r"(?i)(?:api_key|access_token|secret_key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{20,})['\"]?"
        }

    def sanitize_prompt_payload(self, raw_prompt: str) -> Dict[str, Any]:
        """
        Interprets prompt input text, redacts identified PII entities, and records telemetry.
        """
        start_time = time.perf_counter()
        sanitized_text = raw_prompt
        redaction_manifest: List[Dict[str, str]] = []

        # Iterate over configured pattern detectors to scrub matches
        for entity_type, pattern in self.pii_patterns.items():
            matches = re.finditer(pattern, sanitized_text)
            for match in matches:
                detected_value = match.group(0)
                mask_token = f"[REDACTED_{entity_type}]"
                
                # Log detection telemetry without exposing raw PII in state variables
                redaction_manifest.append({
                    "entity_type": entity_type,
                    "character_length": len(detected_value),
                    "mask_applied": mask_token
                })

                # Perform in-place sanitization replacement
                sanitized_text = sanitized_text.replace(detected_value, mask_token)

        execution_time = time.perf_counter() - start_time
        total_redactions = len(redaction_manifest)

        return {
            "verdict": " Sanitized" if total_redactions > 0 else " Clean (No PII Detected)",
            "sanitized_prompt": sanitized_text,
            "telemetry": {
                "total_entities_redacted": total_redactions,
                "redaction_details": redaction_manifest,
                "overhead_seconds": f"{execution_time:.7f}"
            }
        }

if __name__ == "__main__":
    print(" Initializing Phase 5: Day 51 Data Loss Prevention (DLP) Engine...")
    dlp_engine = DataLossPreventionEngine()

    # Simulation: A prompt containing multiple sensitive PII data types
    user_input_with_pii = (
        "Please look up user account associated with email john.doe@enterprise.com "
        "and SSN 123-45-6789. Their contact phone is +1 (555) 019-2831. "
        "Use secret_key = 'sk_live_99x_alpha_key_sample_token'."
    )

    print("\n Processing Raw Input Payload Through DLP Sanitizer:")
    result = dlp_engine.sanitize_prompt_payload(user_input_with_pii)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))