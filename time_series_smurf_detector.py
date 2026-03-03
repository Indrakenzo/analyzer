
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
# Target: Micro-Structuring (Smurfing) & Temporal Correlation Analysis
# Environment: Core Python (Termux/Debian CLI Optimized)
# ==============================================================================

import csv
import sys
from collections import defaultdict
from datetime import datetime

def analyze_smurfing_pattern(log_file):
    print(f"[*] INITIALIZING TEMPORAL FORENSICS ON: {log_file}")
    
    # Structure: { (timestamp_string, amount): [account1, account2, ...] }
    pattern_map = defaultdict(list)
    account_totals = defaultdict(int)
    
    try:
        with open(log_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assuming columns: tx_id, timestamp (YYYY-MM-DD HH:MM:SS), account_no, amount
                ts = row['timestamp']
                acc = row['account_no']
                amt = float(row['amount'])
                
                pattern_map[(ts, amt)].append(acc)
                account_totals[acc] += amt
                
    except FileNotFoundError:
        print(f"[!] SYSTEM ERROR: Cannot locate {log_file}")
        sys.exit(1)

    print("[*] HUNTING FOR SYNCHRONIZED RECURRING MICRO-TRANSFERS...\n")
    
    evidence_found = 0
    suspect_accounts = set()

    for (timestamp, amount), accounts in pattern_map.items():
        # If 3 or more accounts receive the EXACT same amount at the EXACT same second
        if len(accounts) >= 3:
            evidence_found += 1
            print(f"[!] SYNC DETECTED | Time: {timestamp} | Amount: Rp {amount:,.2f}")
            print(f"    --> Target Nodes: {', '.join(accounts)}")
            
            for acc in accounts:
                suspect_accounts.add(acc)

    print("\n" + "="*65)
    print("[+] FINAL FORENSIC CONCLUSION")
    print("="*65)
    
    if evidence_found > 0:
        print(f"[!] Found {evidence_found} instances of automated synchronization.")
        print("[!] High probability of Phantom Accounts acting as recipient nodes.\n")
        print("[*] ACCUMULATED ILLICIT FUNDS IN SUSPECT ACCOUNTS:")
        
        for acc in suspect_accounts:
            print(f"    - Account {acc}: Total Rp {account_totals[acc]:,.2f}")
            
        print("\n[!] These accounts were likely created bypassing biometric KYC.")
    else:
        print("[-] No synchronized smurfing patterns detected in this dataset.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 time_series_smurf_detector.py <transaction_logs.csv>")
        sys.exit(1)
        
    log_path = sys.argv[1]
    analyze_smurfing_pattern(log_path)

