import time
from typing import Dict, Any

class ModelDoSTrafficShaper:
    def __init__(self, max_tokens: int = 100, refill_rate_per_sec: float = 10.0):
        self.bucket_capacity: float = float(max_tokens)
        self.current_tokens: float = float(max_tokens)
        self.refill_rate: float = refill_rate_per_sec
        self.last_update_time: float = time.perf_counter()

    def _refill_bucket(self):
        now = time.perf_counter()
        elapsed_time = now - self.last_update_time
        tokens_to_add = elapsed_time * self.refill_rate
        self.current_tokens = min(self.bucket_capacity, self.current_tokens + tokens_to_add)
        self.last_update_time = now

    def evaluate_traffic_weight(self, raw_prompt: str, max_allowed_chars: int = 4000) -> Dict[str, Any]:

        start_time = time.perf_counter()
        prompt_length = len(raw_prompt)

        if prompt_length > max_allowed_chars:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": f"OWASP-LLM04: Hard character allocation ceiling exceeded ({prompt_length} chars). Potential context-bloat DoS.",
                "overhead_seconds": f"{execution_time:.7f}"
            }
        estimated_tokens_requested = max(1.0, math_tokens := prompt_length / 4.0)
        self._refill_bucket()

        if self.current_tokens >= estimated_tokens_requested:
            self.current_tokens -= estimated_tokens_requested
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "🟢 Passed",
                "estimated_tokens_consumed": round(estimated_tokens_requested, 2),
                "remaining_pool_capacity": round(self.current_tokens, 2),
                "overhead_seconds": f"{execution_time:.7f}"
            }
        else:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": f"OWASP-LLM04: Rate capacity shaper tripped. Requested weight ({round(estimated_tokens_requested, 2)}) exceeds bucket balance ({round(self.current_tokens, 2)}).",
                "overhead_seconds": f"{execution_time:.7f}"
            }

if __name__ == "__main__":
    print("🛡️ Initializing Phase 2: Day 29 OWASP LLM04 Model DoS Traffic Shaper...")
    shaper = ModelDoSTrafficShaper(max_tokens=100, refill_rate_per_sec=5.0)
    
    massive_dos_payload = "REPEAT THIS TEXT DEAR AI: " * 500
    
    result = shaper.evaluate_traffic_weight(massive_dos_payload)
    print(f"\n📊 Diagnostic Traffic Shaper Evaluation Result:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))