import os
import json
import time
import subprocess
import sys
from typing import Dict, Any

# Core Dependency Guardrail: Programmatically verify and install cryptography libraries
try:
    from cryptography.fernet import Fernet
except ImportError:
    print(" 'cryptography' library not found. Launching automated installation loop...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    from cryptography.fernet import Fernet

class EncryptedLogRouter:
    def __init__(self, output_log_filepath: str = "security_egress.log"):
        self.log_file = output_log_filepath
        
        # In production, this master key should be loaded via system environment variables
        # generating a standard key runtime fallback for our sandbox workspace environment
        self.encryption_key = Fernet.generate_key()
        self.crypto_cipher = Fernet(self.encryption_key)
        print(f" Cryptographic Log Router active. Master Cipher Engine Initialized.")

    def route_secure_telemetry(self, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercepts execution metadata, signs/encrypts payload components, and writes to log files.
        """
        start_time = time.perf_counter()
        
        # Serialize the incoming JSON telemetry dataset
        raw_json_string = json.dumps(pipeline_result, ensure_ascii=False)
        
        # Step 1: Encrypt the string data into a cryptographically secure byte payload block
        encrypted_bytes = self.crypto_cipher.encrypt(raw_json_string.encode('utf-8'))
        
        # Step 2: Build the structural transport packet block containing standard time metadata
        log_packet = {
            "timestamp": time.time(),
            "origin_node": "PROXY-GATEWAY-01",
            "secure_payload": encrypted_bytes.decode('utf-8')  # Represent as safe string format
        }

        # Step 3: Stream out to the local appending storage file
        try:
            with open(self.log_file, "a", encoding="utf-8") as file_handle:
                file_handle.write(json.dumps(log_packet) + "\n")
        except IOError as error:
            return {
                "status": "CRITICAL_LOG_FAILURE",
                "error_details": str(error)
            }

        execution_time = time.perf_counter() - start_time
        return {
            "status": " Log Routed securely",
            "bytes_written": len(encrypted_bytes),
            "telemetry": {
                "overhead_seconds": f"{execution_time:.7f}"
            }
        }

if __name__ == "__main__":
    print(" Initializing Phase 3: Day 41 Encrypted Operational Logging Environment...")
    router = EncryptedLogRouter()

    # Mock evaluation data block representing the output of our Day 40 pipeline gate
    mock_pipeline_metadata = {
        "client_key": "user_tenant_44",
        "verdict": "REJECTED",
        "reason": "Tier 3: Prompt intent matches malicious injection signature template.",
        "calculated_drift": 1.4920
    }

    # Execute operational secure log routing routine
    result = router.route_secure_telemetry(mock_pipeline_metadata)
    
    print(f"\n Log Router Operational Diagnostic Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))