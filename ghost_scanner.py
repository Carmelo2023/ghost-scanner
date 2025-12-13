#!/data/data/com.termux/files/usr/bin/python3

"""
Ghost Hacking Scanner - Version PRO
Authors :
- Kikeba Frédéric Carl
- Vincent Molula

Description : Outil de scan réseau éducatif (Termux friendly)
Version : 1.0.9
"""

import os
import sys
import socket
import ssl
import platform
import requests
import dns.resolver
from shutil import get_terminal_size

# ========================
# CONFIG
# ========================
TIMEOUT = 3
socket.setdefaulttimeout(TIMEOUT)
TERM_WIDTH = get_terminal_size((80, 20)).columns

# ========================
# COLORS
# ========================
class C:
    RESET  = "\033[0m"
    RED    = "\033[31m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    BLUE   = "\033[34m"
    CYAN   = "\033[36m"
    WHITE  = "\033[37m"
    BOLD   = "\033[1m"

# ========================
# LOGO & INFO
# ========================
LOGO = r"""
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██║  ███╗███████║██║   ██║███████╗   ██║
██║   ██║██╔══██║██║   ██║╚════██║   ██║
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
"""

TITLE = "Ghost Hacking Scanner - Version PRO"
AUTHORS = "By Kikeba Frédéric Carl & Vincent Molula"

# ========================
# UTILS
# ========================
def clear():
    os.system("clear")

def pause():
    input(C.YELLOW + "\n[ Appuyez sur Entrée pour continuer ]" + C.RESET)

def center(txt):
    return txt.center(TERM_WIDTH)

def boxed_title(text):
    width = len(text) + 12
    top = "╔" + "═" * width + "╗"
    mid = "║" + text.center(width) + "║"
    bot = "╚" + "═" * width + "╝"
    print(C.BLUE + center(top) + C.RESET)
    print(C.BLUE + center(mid) + C.RESET)
    print(C.BLUE + center(bot) + C.RESET)

def header(title):
    clear()
    print(C.CYAN + C.BOLD + LOGO + C.RESET)
    print(C.WHITE + C.BOLD + center(TITLE) + C.RESET)
    print(C.YELLOW + center(AUTHORS) + C.RESET + "\n")
    boxed_title(title)
    print("")

# ========================
# SCANS
# ========================
def scan_ping():
    header("PING SCAN")
    target = input("Cible : ")
    os.system(f"ping -c 6 {target}")
    pause()

def scan_tcp():
    header("TCP PORT SCAN APPROFONDI")
    target = input("Cible : ")
    for port in range(1, 1025):
        try:
            s = socket.socket()
            s.settimeout(0.4)
            if s.connect_ex((target, port)) == 0:
                print(f"{C.GREEN}[+] TCP {port} OUVERT{C.RESET}")
            s.close()
        except:
            pass
    pause()

def scan_udp():
    header("UDP SCAN APPROFONDI")
    target = input("Cible : ")
    ports = [53,67,68,69,123,137,161,500]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            s.sendto(b"", (target, port))
            s.recvfrom(1024)
            print(f"{C.GREEN}[+] UDP {port} RÉPONSE{C.RESET}")
        except socket.timeout:
            print(f"{C.GREEN}[?] UDP {port} OUVERT / FILTRÉ{C.RESET}")
        except:
            pass
        finally:
            s.close()
    pause()

def scan_ssl():
    header("SSL CERTIFICATE SCAN")
    host = input("Domaine : ")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ss:
                cert = ss.getpeercert()
                print(f"{C.GREEN}[+] SSL actif{C.RESET}")
                print(f"{C.GREEN}Version : {ss.version()}{C.RESET}")
                print(f"{C.GREEN}Cipher : {ss.cipher()}{C.RESET}")
                print(f"{C.GREEN}CN : {cert['subject'][0][0][1]}{C.RESET}")
    except Exception as e:
        print(f"{C.RED}[-] Erreur SSL : {e}{C.RESET}")
    pause()

def scan_tls_versions():
    header("TLS VERSION SCAN COMPLET")
    host = input("Domaine : ")
    versions = {
        "TLSv1.0": ssl.PROTOCOL_TLSv1,
        "TLSv1.1": ssl.PROTOCOL_TLSv1_1,
        "TLSv1.2": ssl.PROTOCOL_TLSv1_2,
        "TLSv1.3": ssl.PROTOCOL_TLS
    }
    for name, proto in versions.items():
        try:
            ctx = ssl.SSLContext(proto)
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((host, 443), timeout=TIMEOUT) as sock:
                with ctx.wrap_socket(sock, server_hostname=host):
                    print(f"{C.GREEN}[+] {name} SUPPORTÉ{C.RESET}")
        except:
            print(f"{C.RED}[-] {name} NON SUPPORTÉ{C.RESET}")
    pause()

def scan_sni():
    header("SNI SCAN")
    host = input("Domaine : ")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host):
                print(f"{C.GREEN}[+] SNI supporté{C.RESET}")
    except Exception as e:
        print(f"{C.RED}[-] SNI erreur : {e}{C.RESET}")
    pause()

def scan_http_headers():
    header("HTTP HEADERS APPROFONDI")
    url = input("URL (https://...) : ")
    try:
        r = requests.get(url, timeout=TIMEOUT)
        print(f"{C.GREEN}[+] Headers détectés{C.RESET}\n")
        for k, v in r.headers.items():
            print(f"{C.GREEN}{k}: {v}{C.RESET}")

        print("\n" + C.BLUE + "Sécurité :" + C.RESET)
        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]
        for h in security_headers:
            if h in r.headers:
                print(f"{C.GREEN}[+] {h} présent{C.RESET}")
            else:
                print(f"{C.RED}[-] {h} manquant{C.RESET}")
    except Exception as e:
        print(f"{C.RED}Erreur HTTP : {e}{C.RESET}")
    pause()

def scan_nslookup():
    header("NS LOOKUP")
    domain = input("Domaine : ")
    try:
        for ns in dns.resolver.resolve(domain, "NS"):
            print(f"{C.GREEN}NS : {ns}{C.RESET}")
    except Exception as e:
        print(f"{C.RED}Erreur NS : {e}{C.RESET}")
    pause()

def scan_whois():
    header("WHOIS LOOKUP")
    target = input("Domaine ou IP : ")
    os.system(f"whois {target}")
    pause()

def system_info():
    header("SYSTEM INFO")
    print(f"{C.GREEN}OS : {platform.system()}{C.RESET}")
    print(f"{C.GREEN}Machine : {platform.machine()}{C.RESET}")
    print(f"{C.GREEN}Python : {sys.version.split()[0]}{C.RESET}")
    pause()

# ========================
# MENU
# ========================
def menu():
    while True:
        header("MENU PRINCIPAL")
        print(C.YELLOW + "[1] Ping Scan" + C.RESET)
        print(C.YELLOW + "[2] TCP Port Scan" + C.RESET)
        print(C.YELLOW + "[3] UDP Scan" + C.RESET)
        print(C.YELLOW + "[4] SSL Scan" + C.RESET)
        print(C.YELLOW + "[5] TLS Versions Scan" + C.RESET)
        print(C.YELLOW + "[6] SNI Scan" + C.RESET)
        print(C.YELLOW + "[7] HTTP Headers Scan" + C.RESET)
        print(C.YELLOW + "[8] NS Lookup" + C.RESET)
        print(C.YELLOW + "[9] WHOIS Lookup" + C.RESET)
        print(C.YELLOW + "[10] System Info" + C.RESET)
        print(C.YELLOW + "[0] Quitter\n" + C.RESET)

        c = input("Choix : ")

        if c == "1": scan_ping()
        elif c == "2": scan_tcp()
        elif c == "3": scan_udp()
        elif c == "4": scan_ssl()
        elif c == "5": scan_tls_versions()
        elif c == "6": scan_sni()
        elif c == "7": scan_http_headers()
        elif c == "8": scan_nslookup()
        elif c == "9": scan_whois()
        elif c == "10": system_info()
        elif c == "0":
            clear()
            print(center("Ghost Hacking Scanner - Fermeture"))
            sys.exit()
        else:
            pause()

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    menu()
