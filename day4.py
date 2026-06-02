blacklisted_ips = ["192.168.1.50", "10.0.0.15", "172.16.254.1"]

print("--- 🚨 PERIMETER FIREWALL LOG ---")
print(f"Current Blacklisted IPs : {blacklisted_ips}")
print(f"Primary Threat Vectors Identified :{blacklisted_ips}")

# adding new ip to blacklist
blacklisted_ips.append("192.168.1.99")
print("\n--- UPDATED FIREWALL BLACKLIST ---")
print(f"Updated blacklisted IPs are : {blacklisted_ips}")

#----------------------------------------------------------------------

user_session = {
    "username" : "shaik",
    "role" : "Security_auditor",
    "Active_status" : "yes",
    "Level" : 5
}

print("\n --- ACTIVE SESSION METADATA ---")
print(f"Authentciated identity :{user_session['username']}")
print(f"Assigned Acess Control Role : {user_session['role']}")
