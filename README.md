# ghost-scanner

pkg update -y && pkg upgrade -y

pkg install -y python git openssl-tool

pkg install -y python-pip

pip install requests dnspython urllib3 certifi idna pysocks

git clone https://github.com/Carmelo2023/ghost-scanner

cd ghost-scanner

ghost
