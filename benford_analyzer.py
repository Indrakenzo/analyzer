
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
# Target: Financial Anomaly Detection via Benford's Law
# Environment: CLI-based, Lightweight Data Analysis
# ==============================================================================

import pandas as pd
import numpy as np
import math
import sys

def benfords_law_expected():
    """Calculate expected frequencies for digits 1-9 based on Benford's Law."""
    return {str(d): math.log10(1 + 1/d) * 100 for d in range(1, 10)}

def get_leading_digit(number):
    """Extract the first non-zero digit of a number."""
    try:
        num_str = str(abs(float(number)))
        for char in num_str:
            if char.isdigit() and char != '0':
                return char
    except ValueError:
        return None
    return None

def analyze_dataset(file_path, column_name):
    """Perform Benford's Law analysis on a specific dataset column."""
    print(f"[*] INITIATING FORENSIC ANALYSIS ON: {file_path}")
    print(f"[*] TARGET COLUMN: {column_name}\n")
    
    try:
        # Load dataset - using engine='c' for efficiency on limited RAM
        df = pd.read_csv(file_path, engine='c')
        
        if column_name not in df.columns:
            print(f"[!] ERROR: Column '{column_name}' not found.")
            sys.exit(1)

        # Extract leading digits
        print("[*] Parsing transactions and extracting leading digits...")
        leading_digits = df[column_name].apply(get_leading_digit).dropna()
        
        # Calculate observed frequencies
        total_count = len(leading_digits)
        observed_counts = leading_digits.value_counts().to_dict()
        
        observed_freq = {str(d): (observed_counts.get(str(d), 0) / total_count) * 100 for d in range(1, 10)}
        expected_freq = benfords_law_expected()

        print("\n[+] ANALYSIS COMPLETE. COMPARING DISTRIBUTIONS:")
        print("-" * 50)
        print(f"{'Digit':<10} | {'Expected (%)':<15} | {'Observed (%)':<15} | {'Variance':<10}")
        print("-" * 50)
        
        anomaly_detected = False
        
        for d in range(1, 10):
            digit = str(d)
            exp = expected_freq[digit]
            obs = observed_freq[digit]
            variance = abs(exp - obs)
            
            # Highlight variance > 3% as a potential anomaly (configurable threshold)
            flag = "<-- ANOMALY" if variance > 3.0 else ""
            if variance > 3.0: anomaly_detected = True
            
            print(f"{digit:<10} | {exp:<15.2f} | {obs:<15.2f} | {variance:<10.2f} {flag}")
            
        print("-" * 50)
        
        if anomaly_detected:
            print("\n[!] CRITICAL WARNING: Significant deviations detected.")
            print("[!] High probability of dataset manipulation or fraudulent transaction generation.")
            print("[!] ACTION REQUIRED: Deep audit on transactions starting with anomalous digits.")
        else:
            print("\n[+] Data conforms to Benford's Law. No immediate structural manipulation detected.")

    except Exception as e:
        print(f"[!] SYSTEM ERROR: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 benford_analyzer.py <dataset.csv> <column_name>")
        sys.exit(1)
        
    target_csv = sys.argv[1]
    target_col = sys.argv[2]
    
    analyze_dataset(target_csv, target_col)

