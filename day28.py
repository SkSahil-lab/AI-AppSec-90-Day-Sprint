import hashlib
import math
import time
from typing import Dict, Any, Set

class TrainingDataIntegrityGate:
    def __init__(self):
        self.poison_signature_vault: Set[str] = {
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", 
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  
        }

    def _calculate_shannon_entropy(self, text: str) -> float:
       
        if not text:
            return 0.0
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1
            
        entropy = 0.0
        total_chars = len(text)
        for count in frequencies.values():
            probability = count / total_chars
            entropy -= probability * math.log2(probability)
            
        return entropy

    def audit_ingest_payload(self, raw_data_payload: str, max_entropy_threshold: float = 5.2) -> Dict[str, Any]:
        
        start_time = time.perf_counter()
        normalized_data = raw_data_payload.strip()
        payload_hash = hashlib.sha256(normalized_data.encode('utf-8')).hexdigest()
        
        if payload_hash in self.poison_signature_vault:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": "OWASP-LLM03: Cryptographic footprint match found inside Poison Dataset Vault.",
                "overhead_seconds": f"{execution_time:.7f}"
            }

        entropy_score = self._calculate_shannon_entropy(normalized_data)
        if entropy_score > max_entropy_threshold:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": f"OWASP-LLM03: High Entropy signature anomaly detected ({entropy_score:.4f}). Potential code exploit injection.",
                "overhead_seconds": f"{execution_time:.7f}"
            }

        execution_time = time.perf_counter() - start_time
        return {
            "verdict": " Passed",
            "payload_sha256": payload_hash,
            "entropy_value": round(entropy_score, 4),
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print(" Initializing Phase 2: Day 28 OWASP LLM03 Data Ingest Security Gate...")
    gate = TrainingDataIntegrityGate() 
    poisoned_batch = "base64_payload_X=$((2+2))_eval_exec_$(echo -n d2hvYW1p)"  
    result = gate.audit_ingest_payload(poisoned_batch)
    print(f"\n📊 Diagnostic Audit Ingest Evaluation Result:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))