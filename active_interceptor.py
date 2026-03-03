
# ==============================================================================
#  __      __ _____  _____  _____  _               _   _  _______  ______ 
#  \ \    / /|_   _|/ ____||_   _|| |             /\  | \ | ||__   __||  ____|
#   \ \  / /   | | | |  __   | |  | |            /  \ |  \| |   | |   | |__   
#    \ \/ /    | | | | |_ |  | |  | |           / /\ \| . ` |   | |   |  __|  
#     \  /    _| |_| |__| | _| |_ | |____      / ____ \ |\  |   | |   | |____ 
#      \/    |_____|\_____||_____||______|    /_/    \_\_| \_|   |_|   |______|
# 
#  VIGILANTE - Scutum in tenebris, ensis pro inermibus
# ==============================================================================
# Target: Real-Time Log Tailing & Automated Account Freezing
# Environment: Linux CLI / Termux (Lightweight Daemon)
# ==============================================================================

import time
import json
import urllib.request
import urllib.error
import sys
import os

# Configuration for the Bank's Internal API (Simulated Manokwari Node)
INTERNAL_ADMIN_API = "http://10.50.2.100:8080/api/v1/admin/accounts/"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # Harvested Admin Token

# Known Corruptor Source Accounts (The 'Whales')
TARGET_SYNDICATE_ACCOUNTS = ["00918273645", "00988776655", "00112233445"]

# Local vault to store intercepted transaction evidence
EVIDENCE_VAULT = "intercepted_evidence.log"

def freeze_account(account_id):
    """
    Sends an unauthorized administrative API call to freeze the corruptor's account.
    """
    print(f"\n[!] INITIATING TACTICAL LOCKDOWN ON ACCOUNT: {account_id}")
    url = f"{INTERNAL_ADMIN_API}{account_id}/status"
    
    payload = json.dumps({
        "status": "FROZEN",
        "reason": "CRITICAL_FRAUD_INTERVENTION_VIGILANTE",
        "freeze_code": 999
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', AUTH_TOKEN)
    
    try:
        # Firing the forged request
        response = urllib.request.urlopen(req, timeout=3)
        if response.status in [200, 201, 204]:
            print(f"[+] SUCCESS: Account {account_id} is now FROZEN. Operations halted.")
        else:
            print(f"[-] WARNING: Unexpected API response code: {response.status}")
    except Exception as e:
        print(f"[-] API INTERVENTION FAILED: Target infrastructure might be filtering. {str(e)}")

def log_evidence(transaction_data):
    """
    Copies the transaction trail securely to our local drive.
    """
    with open(EVIDENCE_VAULT, "a") as vault:
        vault.write(transaction_data + "\n")
    print(f"[+] Evidence secured in {EVIDENCE_VAULT}")

def tail_and_intercept(log_file):
    """
    Tails the active transaction log file continuously (like 'tail -f').
    Consumes almost zero RAM.
    """
    print(f"[*] DAEMON ONLINE: Intercepting stream from {log_file}...")
    
    try:
        with open(log_file, 'r') as file:
            # Go to the end of the file
            file.seek(0, os.SEEK_END)
            
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1) # Brief pause to prevent CPU spiking
                    continue
                
                # Assume logs are written in JSON format by the bank's API Gateway
                try:
                    data = json.loads(line.strip())
                    source_acc = data.get("source_account")
                    
                    if source_acc in TARGET_SYNDICATE_ACCOUNTS:
                        print("!"*60)
                        print("[CRITICAL] HOSTILE TRANSACTION DETECTED IN REAL-TIME")
                        print(f"    --> Source : {source_acc}")
                        print(f"    --> Amount : Rp {data.get('amount', 0):,}")
                        print(f"    --> Target : {data.get('target_account', 'UNKNOWN')}")
                        print("!"*60)
                        
                        # 1. Copy the trail
                        log_evidence(line.strip())
                        
                        # 2. Lock their movement immediately
                        freeze_account(source_acc)
                        
                except json.JSONDecodeError:
                    pass # Skip unparseable lines
                    
    except FileNotFoundError:
        print(f"[!] ERROR: Log stream {log_file} not found. Check mounting point.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] INTERCEPTOR OFFLINE. Going dark.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 active_interceptor.py <path_to_live_api_log>")
        sys.exit(1)
        
    target_stream = sys.argv[1]
    tail_and_intercept(target_stream)
