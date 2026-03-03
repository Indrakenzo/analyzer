
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
# Target: Asynchronous Subnet & Infrastructure Mapper
# Environment: Termux / Kali Linux (Non-Root TCP Connect Scan)
# ==============================================================================

import asyncio
import sys
import ipaddress

# Target Ports identifying Critical Infrastructure
TARGET_PORTS = [
    22,    # SSH (Jump Servers/Admin)
    80,    # HTTP (Web Panels)
    443,   # HTTPS (Secure APIs)
    502,   # Modbus TCP (ICS/SCADA)
    3306,  # MySQL (Database)
    8080   # Alt HTTP (API Endpoints)
]

async def scan_port(ip, port, timeout=0.5):
    """
    Attempts an asynchronous TCP connection to a specific IP and port.
    Uses strict timeout to prevent thread blocking and memory leaks.
    """
    try:
        # asyncio.open_connection is lightweight and non-blocking
        coro = asyncio.open_connection(str(ip), port)
        reader, writer = await asyncio.wait_for(coro, timeout=timeout)
        
        print(f"[+] INFRASTRUCTURE DETECTED: {ip}:{port} [STATE: OPEN]")
        
        # Close connection gracefully to avoid filling target's connection table (stealth)
        writer.close()
        await writer.wait_closed()
        return True
        
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        # Port is closed, filtered, or host is down. Ignore silently to keep logs clean.
        return False

async def scan_subnet(subnet_str):
    print(f"[*] INITIATING STEALTH RECONNAISSANCE ON SUBNET: {subnet_str}")
    print(f"[*] TARGET PORTS: {TARGET_PORTS}")
    print("[*] Launching asynchronous probes...\n")
    
    try:
        network = ipaddress.ip_network(subnet_str, strict=False)
    except ValueError as e:
        print(f"[!] FORMAT ERROR: {e}. Use CIDR notation (e.g., 10.50.2.0/24)")
        sys.exit(1)

    tasks = []
    # Iterate through all usable hosts in the subnet
    for ip in network.hosts():
        for port in TARGET_PORTS:
            # Create a task for each IP:Port combination
            tasks.append(asyncio.create_task(scan_port(ip, port)))
            
    # Execute all scanning tasks concurrently
    await asyncio.gather(*tasks)
    print("\n[*] SCAN COMPLETE. Awaiting further tactical instructions.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 stealth_mapper.py <subnet_in_cidr>")
        print("Example: python3 stealth_mapper.py 10.50.2.0/24")
        sys.exit(1)
        
    target_subnet = sys.argv[1]
    
    # Python 3.7+ Async execution
    try:
        asyncio.run(scan_subnet(target_subnet))
    except KeyboardInterrupt:
        print("\n[!] SCAN ABORTED BY USER.")
        sys.exit(0)
