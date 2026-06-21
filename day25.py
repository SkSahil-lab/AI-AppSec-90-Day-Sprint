import time
import json
import uuid
from typing import Dict, Any, List

class DiagnosticDashboard:
    def __init__(self):
        self.metrics_log: List[Dict[str, Any]] = []

    def compile_sprint_telemetry(self, payload_id: str, layers_executed: List[str], latencies: Dict[str, float], status: str, violation: str = None) -> Dict[str, Any]:
        total_latency = sum(latencies.values())
        
        diagnostic_record = {
            "transaction_id": payload_id,
            "timestamp": time.time(),
            "status": status,
            "violation_detected": violation,
            "pipeline_summary": {
                "active_layers_checked": len(layers_executed),
                "total_overhead_ms": round(total_latency * 1000, 4),
            },
            "layer_latency_breakdown_seconds": {
                layer: f"{lat:.7f}" for layer, lat in latencies.items()
            }
        }
        
        self.metrics_log.append(diagnostic_record)
        return diagnostic_record

if __name__ == "__main__":
    print(" Initializing Day 25 Diagnostic Integration Dashboard...")
    dashboard = DiagnosticDashboard()
    
    mock_id = str(uuid.uuid4())
    mock_layers = ["Layer 4", "Layer 5", "Layer 6", "Layer 7", "Layer 8"]
    
    mock_latencies = {
        "Layer 4_RateLimiter": 0.0000021,
        "Layer 5_VolumeThrottler": 0.0000015,
        "Layer 6_SchemaGuard": 0.0000166,
        "Layer 7_InputSanitizer": 0.0000309,
        "Layer 8_SignatureBlocklist": 0.0000069
    }
    
    report = dashboard.compile_sprint_telemetry(
        payload_id=mock_id,
        layers_executed=mock_layers,
        latencies=mock_latencies,
        status="Passed" 
    )
    
    print("\n📊 Generated Live Diagnostic Payload Summary:")
    print(json.dumps(report, indent=2, ensure_ascii=False))