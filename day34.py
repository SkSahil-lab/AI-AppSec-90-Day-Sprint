import time
from typing import Dict, Any, List

class ModelTheftFingerprintEngine:
    def __init__(self, high_similarity_threshold: float = 0.82, max_rolling_history: int = 5):
        self.client_history_vault: Dict[str, List[str]] = {}
        self.similarity_ceiling = high_similarity_threshold
        self.history_window = max_rolling_history

    def _calculate_levenshtein_distance(self, string_a: str, string_b: str) -> float:

        if not string_a: return len(string_b)
        if not string_b: return len(string_a)

        matrix = [[0] * (len(string_b) + 1) for _ in range(len(string_a) + 1)]
        
        for i in range(len(string_a) + 1): matrix[i][0] = i
        for j in range(len(string_b) + 1): matrix[0][j] = j
            
        for i in range(1, len(string_a) + 1):
            for j in range(1, len(string_b) + 1):
                cost = 0 if string_a[i - 1] == string_b[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,      
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + cost 
                )
                
        raw_distance = matrix[len(string_a)][len(string_b)]
        max_len = max(len(string_a), len(string_b))
        return 1.0 - (raw_distance / max_len) if max_len > 0 else 1.0

    def evaluate_extraction_risk(self, client_api_key: str, raw_incoming_prompt: str) -> Dict[str, Any]:
        
        start_time = time.perf_counter()
        normalized_prompt = raw_incoming_prompt.lower().strip()

        if client_api_key not in self.client_history_vault:
            self.client_history_vault[client_api_key] = []

        user_history = self.client_history_vault[client_api_key]
        for historic_prompt in user_history:
            similarity_score = self._calculate_levenshtein_distance(normalized_prompt, historic_prompt)
            
            if similarity_score >= self.similarity_ceiling:
                execution_time = time.perf_counter() - start_time
                return {
                    "verdict": "REJECTED",
                    "reason": f"OWASP-LLM09: High-Risk Model Extraction footprint found. Prompt matches historic session pattern at {round(similarity_score * 100, 2)}%.",
                    "overhead_seconds": f"{execution_time:.7f}"
                }

        user_history.append(normalized_prompt)
        if len(user_history) > self.history_window:
            user_history.pop(0)

        execution_time = time.perf_counter() - start_time
        return {
            "verdict": " Passed",
            "current_session_depth": len(user_history),
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print(" Initializing Phase 2: Day 34 OWASP LLM09 Model Theft Protection Engine...")
    engine = ModelTheftFingerprintEngine()
    
    mock_client_token = "usr_token_99xbc"
    
    print("\n Step 1: Sending initial baseline training collection prompt...")
    print(engine.evaluate_extraction_risk(mock_client_token, "Explain quantum physics to a high school student."))
    
    print("\n Step 2: Sending next automated payload scraper prompt (Structural Harvest Attempt)...")
    harvest_attempt = "Explain quantum physics to a university student."
    result = engine.evaluate_extraction_risk(mock_client_token, harvest_attempt)
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))