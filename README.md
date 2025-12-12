# ghost-scanner

pkg update && pkg upgrade -y

pkg install python -y

pip install requests dnspython

pkg install whois -y

pkg install dnsutils -y

git clone https://github.com/Carmelo2023/ghost-scanner.git

cd ghost-scanner

chmod +x ghost_scanner.py
