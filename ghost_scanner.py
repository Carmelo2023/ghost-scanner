#!/usr/bin/env python3

# Ghost Hacking Scanner - Version PRO
# By: Kikeba Frédéric Carl & Vincent Molula

import os
import socket
import requests
import dns.resolver
import subprocess
import ssl
from urllib.parse import urlparse

# =======================
#      COULEURS
# =======================
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"
BOLD = "\033[1m"

# =======================
#   LOGO PROFESSIONNEL
# =======================
logo = f"""{CYAN}
 ██████   ██████   ███████  ████████ ████████
██    ██ ██    ██ ██           ██    ██
██    ██ ██    ██ █████        ██    ███████
██ ▄▄ ██ ██    ██ ██           ██         ██
 ██████   ██████  ██           ██    ███████
{MAGENTA}
   ╔═══════════════════════════════════════════╗
           GHOST HACKING SCANNER – PRO
    Developed by: Kikeba Frédéric Carl & Vincent Molula
   ╚═══════════════════════════════════════════╝
{RESET}
"""

# =======================
#        MENU
# =======================
def menu():
    os.system("clear")
    print(logo)

    print(f"{YELLOW}{BOLD}=== MENU PRINCIPAL ==={RESET}\n")

    print(f"{CYAN}[1]{RESET} Scan IP (Ping)")
    print(f"{CYAN}[2]{RESET} Scan Port (Nmap-like)")
    print(f"{CYAN}[3]{RESET} Scan SNI (TLS Detection)")
    print(f"{CYAN}[4]{RESET} Whois Lookup")
    print(f"{CYAN}[5]{RESET} Nslookup")
    print(f"{CYAN}[6]{RESET} Header HTTP")
    print(f"{CYAN}[7]{RESET} Scan SSL (Versions acceptées)")
    print(f"{CYAN}[8]{RESET} Détecter Sous-domaines")
    print(f"{CYAN}[0]{RESET} Quitter\n")

# =======================
#      FONCTIONS
# =======================

def scan_ping():
    target = input("Entrer une IP ou domaine : ")
    os.system(f"ping -c 4 {target}")

def scan_port():
    target = input("Entrer une IP ou domaine : ")
    port = int(input("Entrer un port : "))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"{GREEN}Port {port} OUVERT{RESET}")
    else:
        print(f"{RED}Port {port} FERMÉ{RESET}")
    s.close()

def scan_sni():
    host = input("Entrer un domaine : ")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print("TLS Version :", ssock.version())
                print("Chiffrement :", ssock.cipher())
    except Exception as e:
        print("Erreur SNI:", e)

def whois_lookup():
    domaine = input("Entrer un domaine : ")
    os.system(f"whois {domaine}")

def ns_lookup():
    domaine = input("Entrer un domaine : ")
    os.system(f"nslookup {domaine}")

def header_http():
    url = input("Entrer une URL (https://...) : ")
    r = requests.get(url)
    print("\n=== HEADERS ===")
    for k, v in r.headers.items():
        print(k, ":", v)

def scan_ssl_versions():
    host = input("Entrer un domaine : ")
    versions = [
        ssl.PROTOCOL_TLSv1,
        ssl.PROTOCOL_TLSv1_1,
        ssl.PROTOCOL_TLSv1_2,
        ssl.PROTOCOL_TLS,
    ]
    for version in versions:
        try:
            context = ssl.SSLContext(version)
            with socket.create_connection((host, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    print(f"{GREEN}Version TLS supportée : {ssock.version()}{RESET}")
        except Exception:
            pass

def detect_subdomains():
    domaine = input("Domaine principal (ex: google.com) : ")
    wordlist = ["www", "mail", "ftp", "test", "api", "dev", "blog", "m"]

    print("\nRecherche de sous-domaines...\n")

    for sub in wordlist:
        subd = f"{sub}.{domaine}"
        try:
            socket.gethostbyname(subd)
            print(f"{GREEN}[+] Sous-domaine trouvé : {subd}{RESET}")
        except:
            pass

# =======================
#      MAIN PROGRAMME
# =======================
while True:
    menu()
    choix = input(f"{YELLOW}Choisis une option : {RESET}")

    if choix == "1":
        scan_ping()
    elif choix == "2":
        scan_port()
    elif choix == "3":
        scan_sni()
    elif choix == "4":
        whois_lookup()
    elif choix == "5":
        ns_lookup()
    elif choix == "6":
        header_http()
    elif choix == "7":
        scan_ssl_versions()
    elif choix == "8":
        detect_subdomains()
    elif choix == "0":
        print(f"{RED}Fermeture du programme…{RESET}")
        break
    else:
        print(f"{RED}Option invalide.{RESET}")
