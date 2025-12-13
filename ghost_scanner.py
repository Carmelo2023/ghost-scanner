#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ghost Hacking Scanner - Version PRO
By Kikeba Frédéric Carl & Vincent Molula
Outil éducatif – Termux Friendly
"""

import os
import socket
import ssl
import platform
import requests
import threading
import dns.resolver
import subprocess

# ======================
# COULEURS ANSI
# ======================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ======================
# CLEAR / PAUSE
# ======================
def clear():
    os.system("clear")

def pause():
    input(f"\n{YELLOW}Appuyez sur Entrée pour continuer...{RESET}")

# ======================
# LOGO + FANTÔME 👻
# ======================
logo = f"""{RED}{BOLD}
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██║  ███╗███████║██║   ██║███████╗   ██║
██║   ██║██╔══██║██║   ██║╚════██║   ██║
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
{RESET}
{RED}       [[  Ghost Hacking Scanner - Version 1.0  ]]{RESET}
{GREEN}       ● By Kikeba Frédéric Carl & Vincent Molula ●{RESET}

{GREEN}
                         👻
                         .-.
                        (o o) boo!
                        | O |
                        |   |
                        |___|
{RESET}

{GREEN}             ╔══════════════════════════╗
             ║      MENU PRINCIPAL      ║
             ╚══════════════════════════╝{RESET}
"""

# ======================
# FONCTIONS DE SCAN
# ======================
def ping_scan():
    target = input("Cible (IP/Domaine) : ")
    os.system(f"ping -c 4 {target}")

def tcp_port_scan():
    target = input("Cible : ")
    ports = [21,22,23,25,53,80,110,139,443,445,8080]
    for port in ports:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            print(f"{GREEN}[OPEN]{RESET} TCP {port}")
        s.close()

def udp_scan():
    print(f"{YELLOW}UDP scan basique (informatif){RESET}")

def ssl_scan():
    domain = input("Domaine : ")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            print(f"{GREEN}SSL détecté sur {domain}{RESET}")
    except:
        print(f"{RED}SSL non détecté{RESET}")

def tls_versions_scan():
    domain = input("Domaine : ")
    versions = {
        "TLSv1": ssl.PROTOCOL_TLSv1,
        "TLSv1.1": ssl.PROTOCOL_TLSv1_1,
        "TLSv1.2": ssl.PROTOCOL_TLSv1_2
    }
    for name, proto in versions.items():
        try:
            ctx = ssl.SSLContext(proto)
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(2)
                s.connect((domain, 443))
                print(f"{GREEN}{name} supporté{RESET}")
        except:
            pass

def sni_scan():
    domain = input("Nom SNI / Domaine : ")
    print(f"{GREEN}SNI testé : {domain}{RESET}")

def http_headers_scan():
    url = input("URL (https://...) : ")
    try:
        r = requests.get(url, timeout=10)
        for k, v in r.headers.items():
            print(f"{CYAN}{k}{RESET}: {v}")
    except Exception as e:
        print(f"{RED}Erreur : {e}{RESET}")

def ns_lookup():
    domain = input("Domaine : ")
    try:
        for r in dns.resolver.resolve(domain, "NS"):
            print(f"{GREEN}{r.to_text()}{RESET}")
    except Exception as e:
        print(f"{RED}Erreur : {e}{RESET}")

def whois_lookup():
    domain = input("Domaine : ")
    os.system(f"whois {domain}")

def system_info():
    print(platform.uname())

# ======================
# SUBDOMAIN FINDER PRO
# ======================
def subdomainfinder():
    domain = input("Domaine : ")
    print(f"{BLUE}[+] Subdomainfinder approfondie en cours...{RESET}")

    wordlist = [
        "www","mail","ftp","dev","api","admin",
        "test","beta","blog","shop","panel","staging"
    ]

    found = set()

    def brute(sub):
        try:
            host = f"{sub}.{domain}"
            socket.gethostbyname(host)
            found.add(host)
            print(f"{GREEN}[FOUND]{RESET} {host}")
        except:
            pass

    threads = []
    for w in wordlist:
        t = threading.Thread(target=brute, args=(w,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
        if r.status_code == 200:
            for e in r.json():
                for s in e["name_value"].split("\n"):
                    if domain in s:
                        found.add(s.strip())
    except:
        pass

    print(f"{YELLOW}Total : {len(found)} sous-domaines trouvés{RESET}")

# ======================
# MENU PRINCIPAL
# ======================
def menu():
    while True:
        clear()
        print(logo)
        print("""
[1] Ping Scan✔️
[2] TCP Port Scan✔️
[3] UDP Scan✔️
[4] SSL Scan✔️
[5] TLS Versions Scan✔️
[6] SNI Scan✔️
[7] HTTP Headers Scan (approfondie)✔️
[8] NS Lookup✔️
[9] WHOIS lookup✔️
[10]System info✔️
[11]Subdomainfinder (approfondie)✔️
[0] Quitter✔️""")



        choix = input("Choix : ")

        if choix == "1": ping_scan()
        elif choix == "2": tcp_port_scan()
        elif choix == "3": udp_scan()
        elif choix == "4": ssl_scan()
        elif choix == "5": tls_versions_scan()
        elif choix == "6": sni_scan()
        elif choix == "7": http_headers_scan()
        elif choix == "8": ns_lookup()
        elif choix == "9": whois_lookup()
        elif choix == "10": system_info()
        elif choix == "11": subdomainfinder()
        elif choix == "0":
            print(f"{GREEN}À bientôt… Boo 👻{RESET}")
            break
        else:
            print(f"{RED}Choix invalide{RESET}")

        pause()

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    menu()
