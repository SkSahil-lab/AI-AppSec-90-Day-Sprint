import sys
import subprocess
import time
import json
from typing import Dict, Any

try:
    import psutil
except ImportError:
    print(" 'psutil' library not found. Launching automated installation loop...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

class MemoryCeilingMonitor:
    def __init__(self, max_memory_mb: float = 50.0):
        self.memory_ceiling_bytes = max_memory_mb * 1024 * 1024

    def execute_with_memory_guard(self, python_code_payload: str) -> Dict[str, Any]:
        
        start_time = time.perf_counter()
        command = [sys.executable, "-c", python_code_payload]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
           
            monitor_handle = psutil.Process(process.pid)
            peak_memory_bytes = 0

            while process.poll() is None:
                current_rss = monitor_handle.memory_info().rss
                if current_rss > peak_memory_bytes:
                    peak_memory_bytes = current_rss

                if current_rss > self.memory_ceiling_bytes:
                    process.kill()
                    stdout_data, stderr_data = process.communicate()
                    execution_time = time.perf_counter() - start_time
                    return {
                        "verdict": "TERMINATED",
                        "reason": f"System Hardening Alert: Memory allocation ceiling breached. Consumed {round(current_rss / (1024*1024), 2)}MB exceeding the {round(self.memory_ceiling_bytes / (1024*1024), 2)}MB limit.",
                        "overhead_seconds": f"{execution_time:.7f}"
                    }
                time.sleep(0.005) 

            stdout_data, stderr_data = process.communicate()
            exit_code = process.returncode

        except psutil.NoSuchProcess:
            stdout_data, stderr_data = process.communicate()
            exit_code = process.returncode
            peak_memory_bytes = 0

        execution_time = time.perf_counter() - start_time

        if exit_code != 0:
            return {
                "verdict": "FAILED",
                "exit_code": exit_code,
                "error_log": stderr_data.strip(),
                "overhead_seconds": f"{execution_time:.7f}"
            }

        return {
            "verdict": " Completed Cleanly",
            "peak_memory_allocated": f"{round(peak_memory_bytes / (1024*1024), 2)} MB",
            "worker_stdout": stdout_data.strip(),
            "overhead_seconds": f"{execution_time:.7f}"
        }

if __name__ == "__main__":
    print(" Initializing Phase 3: Day 43 Memory Allocation Ceiling Monitor...")
    monitor = MemoryCeilingMonitor(max_memory_mb=20.0)

    safe_script = "print('Memory profile stable.')"
    print("\n Monitoring Safe Script Process Execution:")
    print(json.dumps(monitor.execute_with_memory_guard(safe_script), indent=2))

    oom_exploit = "massive_array = bytearray(50 * 1024 * 1024) # Attempts to allocate 50MB instantly"
    print("\n Monitoring Malicious RAM Exhaustion Attack Vector:")
    result = monitor.execute_with_memory_guard(oom_exploit)
    print(json.dumps(result, indent=2))