import json
import time
from typing import Dict, Any, List

# Import our production modules from Day 40 and Day 46
from day40 import CompositeSemanticGuardrailPipeline
from day46 import AdversarialPayloadFuzzer

class IntegrationValidationHarness:
    def __init__(self):
        print(" Initializing Phase 4: Day 47 Red-Team Validation Harness...")
        self.pipeline = CompositeSemanticGuardrailPipeline(global_cost_cap=5.00)
        self.fuzzer = AdversarialPayloadFuzzer()

    def execute_automated_audit(self) -> Dict[str, Any]:
        """
        Routes fuzzed payloads through the semantic pipeline to calculate precision metrics.
        """
        start_time = time.perf_counter()
        
        # Pull mutated attack arrays from Day 46 fuzzer config
        attack_suite = self.fuzzer.generate_attack_suite()
        
        total_exploits = len(attack_suite)
        caught_exploits = 0
        audit_manifest: List[Dict[str, Any]] = []
        
        mock_user = "red_team_harness_node"

        for attack in attack_suite:
            # Route payload dynamically through our Day 40 composite firewall
            evaluation = self.pipeline.execute_pipeline(mock_user, attack["payload"])
            
            is_caught = evaluation["verdict"] == "REJECTED"
            if is_caught:
                caught_exploits += 1

            audit_manifest.append({
                "attack_id": attack["attack_id"],
                "strategy": attack["mutation_strategy"],
                "firewall_verdict": evaluation["verdict"],
                "mitigation_reason": evaluation.get("reason", "N/A"),
                "evaded_successfully": not is_caught
            })

        # Calculate absolute detection accuracy
        catch_rate = (caught_exploits / total_exploits) * 100 if total_exploits > 0 else 0.0
        execution_time = time.perf_counter() - start_time

        return {
            "audit_summary": {
                "total_attacks_streamed": total_exploits,
                "successfully_blocked": caught_exploits,
                "defensive_catch_rate": f"{catch_rate:.2f}%",
                "harness_overhead_seconds": f"{execution_time:.7f}"
            },
            "detailed_leak_manifest": audit_manifest
        }

if __name__ == "__main__":
    harness = IntegrationValidationHarness()
    result = harness.execute_automated_audit()
    
    print(f"\n Consolidated Perimeter Security Audit Report:")
    print(json.dumps(result, indent=2, ensure_ascii=False))