# 👻 Ghost Hacking Scanner

**Ghost Hacking Scanner** est un outil de scan réseau éducatif conçu pour fonctionner parfaitement sur **Termux (Android)**.  
Il permet d’effectuer différents tests réseau à des fins **d’apprentissage et d’audit légal**.

---

## ⚠️ Avertissement légal
Cet outil est destiné **uniquement à des fins éducatives**.  
Toute utilisation sans autorisation explicite sur des systèmes tiers est **illégale**.  
Les auteurs déclinent toute responsabilité en cas de mauvaise utilisation.

---

## 🛠️ Prérequis
- Android avec **Termux**
- Connexion Internet
- Python 3

---

## 🚀 Installation complète (copier-coller)

```bash
pkg update -y && pkg upgrade -y
pkg install -y git python

git clone https://github.com/Carmelo2023/ghost-scanner
cd ghost-scanner

pip install requests dnspython

python ghost_scanner.py
