import time
from typing import Dict, Any

class UnboundedConsumptionTracker:
    def __init__(self, global_daily_budget_usd: float = 50.00):
        self.tenant_spend_ledger: Dict[str, float] = {}
        self.max_daily_budget_usd = global_daily_budget_usd
        self.cost_per_input_token = 0.0000015  
        self.cost_per_output_token = 0.0000020 

    def process_and_ledger_transaction(self, client_api_key: str, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        start_time = time.perf_counter()
        if client_api_key not in self.tenant_spend_ledger:
            self.tenant_spend_ledger[client_api_key] = 0.0

        current_tenant_spend = self.tenant_spend_ledger[client_api_key]

        if current_tenant_spend >= self.max_daily_budget_usd:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": f"OWASP-LLM10: Hard economic allocation threshold reached. Daily account spend cap of ${self.max_daily_budget_usd:.2f} is fully exhausted.",
                "overhead_seconds": f"{execution_time:.7f}"
            }
        input_expense = float(input_tokens) * self.cost_per_input_token
        output_expense = float(output_tokens) * self.cost_per_output_token
        transaction_total_cost = input_expense + output_expense

        if (current_tenant_spend + transaction_total_cost) > self.max_daily_budget_usd:
            execution_time = time.perf_counter() - start_time
            return {
                "verdict": "REJECTED",
                "reason": f"OWASP-LLM10: Request denied. Transaction cost (${transaction_total_cost:.5f}) breaks remaining daily budget margin (${(self.max_daily_budget_usd - current_tenant_spend):.5f}).",
                "overhead_seconds": f"{execution_time:.7f}"
            }

        self.tenant_spend_ledger[client_api_key] += transaction_total_cost
        
        execution_time = time.perf_counter() - start_time
        return {
            "verdict": " Passed",
            "transaction_cost_usd": f"${transaction_total_cost:.6f}",
            "cumulative_day_spend_usd": f"${self.tenant_spend_ledger[client_api_key]:.6f}",
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print(" Initializing Phase 2: Day 35 OWASP LLM10 Cost-Cap Tracker...")
    tracker = UnboundedConsumptionTracker(global_daily_budget_usd=1.00) 
    mock_tenant_token = "client_enterprise_77a"
    
    print("\n Logging transaction 1 (Standard Query):")
    print(tracker.process_and_ledger_transaction(mock_tenant_token, input_tokens=150000, output_tokens=300000))
    
    print("\n Logging transaction 2 (Heavy Looping Attack Vector):")
    result = tracker.process_and_ledger_transaction(mock_tenant_token, input_tokens=400000, output_tokens=500000)
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))