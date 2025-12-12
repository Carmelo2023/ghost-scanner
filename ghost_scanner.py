#!/usr/bin/env python3

# Ghost Hacking Scanner - Version PRO
# By: Kikeba Frédéric Carl

import os
import socket
import requests
import dns.resolver
import subprocess
import ssl
from urllib.parse import urlparse

logo = r"""
 ██████   ██████   ██████  ███████ ████████ ██       ██    ██ ██    ██ ██         ██
██   ███ ██    ██ ██    ██ ███████    ██
██    ██ ██    ██ ██    ██      ██    ██
██████   ██████   ██████  ███████    ██

GHOST HACKING SCANNER - PRO VERSION
By: Kikeba Frédéric Carl
"""

def menu():
    print(logo)
    print("1. Scan IP (Ping)")
    print("2. Scan Port (Nmap-like)")
    print("3. Scan SNI (TLS Detection)")
    print("4. Whois Lookup")
    print("5. Nslookup")
    print("6. Header HTTP")
    print("7. Scan SSL (Versions Acceptées)")
    print("8. Détecter Sous-domaines")
    print("0. Quitter")


# ========================
#   FONCTIONS
# ========================

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
        print(f"Port {port} OUVERT")
    else:
        print(f"Port {port} FERMÉ")
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
    print("=== HEADERS ===")
    for k, v in r.headers.items():
        print(k, ":", v)


def scan_ssl_versions():
    host = input("Entrer un domaine : ")
    versions = [
        ssl.PROTOCOL_TLSv1,
        ssl.PROTOCOL_TLSv1_1,
        ssl.PROTOCOL_TLSv1_2,
        ssl.PROTOCOL_TLS
    ]

    for version in versions:
        try:
            context = ssl.SSLContext(version)
            with socket.create_connection((host, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    print(f"Version TLS supportée : {ssock.version()}")
        except Exception:
            pass


def detect_subdomains():
    domaine = input("Domaine principal (ex: google.com) : ")
    wordlist = ["www", "mail", "ftp", "test", "api", "dev", "m", "blog"]

    print("Recherche de sous-domaines...\n")

    for sub in wordlist:
        subd = f"{sub}.{domaine}"
        try:
            socket.gethostbyname(subd)
            print("[+] Sous-domaine trouvé:", subd)
        except:
            pass


# ========================
#   PROGRAMME PRINCIPAL
# ========================

while True:
    menu()
    choix = input("Choisis une option : ")

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
        break
    else:
        print("Option invalide.")
