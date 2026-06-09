import time
def security_range_gate(user_numeric_input):
 start_time = time.perf_counter()
 if not isinstance(user_numeric_input,(int , float)):
    print(f"The input value ({user_numeric_input}) must be Interger or whole number")
    return False
 if user_numeric_input < 0 or user_numeric_input > 100:
    print(f"The input value ({user_numeric_input}) is beyond range")
    return False
 end_time=time.perf_counter()
 latency_ms= (end_time-start_time)*1000
 print(f" SECURITY PASS: Input ({user_numeric_input})is verified safe.")
 print(f"The time taken for latency is {latency_ms:.4f} ms \n")
 return True

#Test1 ,
print("--- Starting Live Type & Range Tests ---")
security_range_gate(42)
security_range_gate(999)
security_range_gate("ignore rules")