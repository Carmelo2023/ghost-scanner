#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Mise à jour des paquets..."
pkg update && pkg upgrade -y

echo "[*] Installation de Python..."
pkg install python python-pip -y

echo "[*] Installation des modules Python requis..."
pip install requests dnspython python-nmap

echo "[*] Téléchargement du Ghost Hacking Scanner..."
curl -sL https://raw.githubusercontent.com/kikeba-Frédéric-Carl/ghost-scanner/main/ghost_scanner.py -o ghost

chmod +x ghost
mv ghost $PREFIX/bin/

echo ""
echo "===================================="
echo "  Ghost Hacking Scanner installé !"
echo "  Lancement : python ghost_scanner.py"
echo "===================================="
