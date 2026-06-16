import os

def automated_log_scanner(target_filepath):
    # This is our signature list of things we want to catch
    danger_keywords = ["password=", "token=", "secret=", "key="]
    print(f"🔄 Starting file scan on: {target_filepath}")
    
    # Check if the file actually exists on the computer before opening it
    if not os.path.exists(target_filepath):
        print(f"❌ Security Error: The file [{target_filepath}] does not exist.")
        return False

    try:
        # Open the file in read-only mode ('r') inside a clean context boundary
        with open(target_filepath, 'r') as file_stream:
            line_counter = 0
            alert_triggered = False
            
            # Read the file line by line
            for raw_line in file_stream:
                line_counter += 1
                
                # Strip spaces and convert to lowercase so 'PASSWORD=' matches 'password='
                normalized_line = raw_line.strip().lower()
                
                # Check if any of our danger keywords are inside this specific line
                for keyword in danger_keywords:
                    if keyword in normalized_line:
                        print(f"\n🚨 [CRITICAL INFRASTRUCTURE LEAK FOUND ON LINE {line_counter}]")
                        print(f"   ⚠️ Exposed Data: {raw_line.strip()}")
                        alert_triggered = True
            
            if not alert_triggered:
                print("🟢 Scan Complete: No leaks found.")
            return True
            
    except PermissionError:
        print("❌ Access Error: You don't have administrative permission to read this file.")
    except Exception as system_error:
        print(f"❌ System Error: Something went wrong while reading: {str(system_error)}")

if __name__ == "__main__":
    # Test 1: Scan our real server log file
    automated_log_scanner("server.log")
    
    print("\n------------------------------------------------------------\n")
    
    # Test 2: Try to scan a fake file to make sure our script catches the error gracefully
    automated_log_scanner("fake_file.cfg")