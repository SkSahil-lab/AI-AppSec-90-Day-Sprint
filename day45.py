import time
import json
from typing import Dict, Any

class TokenBucketRateBroker:
    def __init__(self, bucket_capacity: int = 10, refill_rate_per_sec: float = 2.0):
        """
        Initializes the Token Bucket memory tracking broker.
        """
        self.capacity = float(bucket_capacity)
        self.refill_rate = refill_rate_per_sec
        
        # State vault tracking user metrics: { client_key: (last_refill_timestamp, current_tokens) }
        self.bucket_vault: Dict[str, tuple] = {}

    def _refresh_and_evaluate_bucket(self, client_key: str) -> float:
        """
        Calculates fluid token refills based on real-world time deltas.
        """
        now = time.time()
        
        if client_key not in self.bucket_vault:
            # Initialize bucket to maximum capacity state on first check
            self.bucket_vault[client_key] = (now, self.capacity)
            return self.capacity

        last_update, tokens = self.bucket_vault[client_key]
        
        # Step 1: Calculate time delta elapsed since last validation tick
        time_delta = max(0.0, now - last_update)
        
        # Step 2: Mathematically compute fractional token refill amount
        refilled_tokens = tokens + (time_delta * self.refill_rate)
        
        # Enforce hard upper bounds corresponding to max capacity limits
        current_tokens = min(self.capacity, refilled_tokens)
        
        # Mutate timestamp tracker state
        self.bucket_vault[client_key] = (now, current_tokens)
        return current_tokens

    def consume_request_token(self, client_key: str) -> Dict[str, Any]:
        """
        Audits user access pacing, consuming a bucket unit if clearance criteria are met.
        """
        start_time = time.perf_counter()
        
        # Refresh state maps dynamically
        available_tokens = self._refresh_and_evaluate_bucket(client_key)
        
        # Step 3: Enforce strict drop barrier if bucket is completely drained
        if available_tokens < 1.0:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": "Infrastructure Alert: Rate limit allocation exhausted. Flooding concurrency threshold exceeded.",
                "overhead_seconds": f"{execution_time:.7f}"
            }

        # Step 4: Consume one operational slot token out of the bucket pool
        last_update, current_tokens = self.bucket_vault[client_key]
        self.bucket_vault[client_key] = (last_update, current_tokens - 1.0)
        
        execution_time = time.perf_counter() - start_time
        return {
            "verdict": " Passed Rate Check",
            "tokens_remaining": int(current_tokens - 1.0),
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print(" Initializing Phase 3: Day 45 Token Bucket Rate Broker...")
    # Setup broker with tight testing constraints: max 3 requests, refills 1 token every 2 seconds
    broker = TokenBucketRateBroker(bucket_capacity=3, refill_rate_per_sec=0.5)
    
    mock_client = "tenant_id_99x"
    
    # Simulation A: Rapid burst query execution loop
    print("\n Simulating immediate high-velocity request surge burst:")
    for i in range(4):
        print(f" Request {i+1}: {broker.consume_request_token(mock_client)['verdict']}")
        
    # Simulation B: Introduce a short cooling interval to witness time-based metric refills
    print("\n Pausing infrastructure execution context for 2.0s to allow token refill...")
    time.sleep(2.0)
    
    print("\n Retrying connection allocation block post-refill:")
    result = broker.consume_request_token(mock_client)
    print(json.dumps(result, indent=2, ensure_ascii=False))