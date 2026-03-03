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
# Target: Automated Smurfing Detection via Timestamp Collision
# Environment: Python Core Library (Ultra-lightweight)
# ==============================================================================

import csv
from collections import defaultdict
import sys

def detect_timestamp_collisions(log_file):
    """
    Parses bank transaction logs to identify exact millisecond collisions,
    proving automated API dispatching for money laundering.
    """
    print(f"[*] INITIATING LOG PARSING: {log_file}")
    
    # Using defaultdict to group transactions by exact timestamp
    collision_map = defaultdict(list)
    
    try:
        with open(log_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Required columns in dump: timestamp_ms, target_account, amount
                ts = row['timestamp_ms']
                acc = row['target_account']
                amt = row['amount']
                
                collision_map[ts].append({'account': acc, 'amount': amt})
                
    except FileNotFoundError:
        print(f"[!] ERROR: {log_file} not found. Check path.")
        sys.exit(1)

    print("[*] ANALYZING TIMESTAMPS FOR AUTOMATED BATCH INJECTIONS...\n")
    
    found_evidence = False
    
    for timestamp, transactions in collision_map.items():
        # If more than 3 transactions happen in the EXACT same millisecond, it's a script.
        if len(transactions) >= 3:
            found_evidence = True
            print("-" * 65)
            print(f"[!] CRITICAL ANOMALY DETECTED AT EXACT TIMESTAMP: {timestamp}")
            print("-" * 65)
            print(f"{'TARGET ACCOUNT':<20} | {'AMOUNT (IDR)':<25}")
            print("-" * 65)
            
            total_laundered = 0
            for txn in transactions:
                print(f"{txn['account']:<20} | Rp {int(txn['amount']):,}")
                total_laundered += int(txn['amount'])
                
            print("-" * 65)
            print(f"[+] TOTAL BATCH EXECUTION AMOUNT: Rp {total_laundered:,}\n")
            print("[!] CONCLUSION: Human execution impossible. Automated API trigger confirmed.")
            
    if not found_evidence:
        print("[-] No synchronized batch executions found in this log chunk.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 timestamp_hunter.py <bank_logs.csv>")
        sys.exit(1)
        
    target_log = sys.argv[1]
    detect_timestamp_collisions(target_log)

