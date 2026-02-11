import socket
import os
from datetime import datetime
import time

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def show_banner():
    banner = f"""{CYAN}
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗      ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║      ╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║       ╚███╔╝ 
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║       ██╔██╗ 
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║      ██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝

        RECON-X v1.0 | Simple Port Scanner
{RESET}
"""
    print(banner)


def is_target_alive(target):
    print(f"{YELLOW}[*] Checking if target is alive...{RESET}")
    response = os.system(f"ping -c 1 {target} > /dev/null 2>&1")
    return response == 0


def scan_ports(target):
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 8080]

    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        139: "NetBIOS",
        443: "HTTPS",
        445: "SMB",
        8080: "HTTP-ALT"
    }

    open_count = 0
    closed_count = 0

    print(f"\n{YELLOW}[*] Starting Port Scan...{RESET}\n")

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))
        service_name = services.get(port, "Unknown")

        if result == 0:
            print(f"{GREEN}[OPEN]   Port {port} ({service_name}){RESET}")
            open_count += 1
        else:
            print(f"{RED}[CLOSED] Port {port} ({service_name}){RESET}")
            closed_count += 1

        sock.close()

    return open_count, closed_count


def main():
    show_banner()
    time.sleep(0.5)

    target = input(f"{CYAN}Enter target IP or domain: {RESET}")

    if not is_target_alive(target):
        print(f"{RED}[-] Target is not reachable. Exiting.{RESET}")
        return

    print(f"{GREEN}[+] Target is alive.{RESET}")
    print(f"{YELLOW}[*] Scan started at: {datetime.now()}{RESET}\n")

    open_count, closed_count = scan_ports(target)

    print(f"\n{CYAN}" + "=" * 50 + f"{RESET}")
    print(f"{GREEN}Open Ports   : {open_count}{RESET}")
    print(f"{RED}Closed Ports : {closed_count}{RESET}")
    print(f"{CYAN}" + "=" * 50 + f"{RESET}")


if __name__ == "__main__":
    main()
