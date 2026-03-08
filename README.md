<div align="center">

# 🐙 OctoCrypt

<img src="https://img.shields.io/badge/Security-AES--256--GCM-black?style=for-the-badge&logo=shield&logoColor=green"/>
<img src="https://img.shields.io/badge/Crypto-Ed25519-black?style=for-the-badge&logo=letsencrypt&logoColor=green"/>
<img src="https://img.shields.io/badge/Python-3.10+-black?style=for-the-badge&logo=python&logoColor=green"/>
<img src="https://img.shields.io/badge/Interface-CLI%20%2B%20GUI-black?style=for-the-badge&logo=windows-terminal&logoColor=green"/>

### 🔐 Professionelle Datei-Verschlüsselung mit moderner Kryptographie

**OctoCrypt** ist ein Sicherheits-Tool zum **Verschlüsseln von Dateien mit AES-256-GCM**,
starken Passwörtern, **digitalen Signaturen (Ed25519)** und **Kompression**.

Entwickelt für Entwickler, Sicherheitsforscher und Power-User.

</div>

---

# ⚡ Features

| Feature                | Beschreibung                     |
| ---------------------- | -------------------------------- |
| 🔐 AES-256-GCM         | Authentifizierte Verschlüsselung |
| 🧠 Passwort-Sicherheit | Komplexitätsprüfung              |
| 📦 Kompression         | `zlib` reduziert Dateigröße      |
| ✍ Digitale Signatur    | `Ed25519` für Integrität         |
| 🖥 Interface           | CLI + GUI                        |
| 🛡 Sicherheitsdesign   | Schutz gegen Manipulation        |

---

# 🧰 Technologien

```
Python 3.10+
AES-256-GCM
Ed25519 Signaturen
zlib Compression
Tkinter GUI
Secure Metadata Format
```

---

# 📦 Installation

```bash
git clone https://github.com/Oktopus-Motor/octocrypt
cd octocrypt

pip install -r requirements.txt
```

---

# 💻 Verwendung (CLI)

## 🔐 Datei verschlüsseln

```bash
python octocrypt.py encrypt secret.txt

password: ********
confirm password: ********

file encrypted -> secret.octo
```

---

## 🔓 Datei entschlüsseln

```bash
python octocrypt.py decrypt secret.octo

password: ********

file decrypted -> secret.txt
```

---

## 🔑 Signaturschlüssel generieren

```bash
python octocrypt.py keygen
```

---

## 🖥 GUI starten

```bash
python octocrypt.py gui
```

---

# 🐧 Nutzung wie ein echtes CLI-Tool

```bash
octocrypt encrypt secret.txt

password: ********

file encrypted -> secret.octo
```

Windows Nutzer können dafür **octocrypt.bat** verwenden.

---

# 📁 Dateiformat `.octo`

Das OctoCrypt-Format wurde für **Sicherheit und Erweiterbarkeit** entwickelt.

```
HEADER
Version

METADATA (JSON)
algorithm
salt
nonce
hash
signature

CIPHERTEXT
AES-256-GCM encrypted data
```

---

# 🛡 Sicherheitsprinzipien

OctoCrypt wurde mit Fokus auf **moderne Kryptographie** entwickelt.

✔ Authentifizierte Verschlüsselung
✔ Integritätsprüfung
✔ Digitale Signatur
✔ Schutz gegen Manipulation

---

# ⚠ Sicherheitshinweise

```
• Passwörter niemals über CLI Argumente übergeben
• Private Ed25519 Schlüssel sicher speichern
• Backups der Schlüssel erstellen
• Nur vertrauenswürdige Systeme verwenden
```

Standardpfad:

```
~/.octocrypt/ed25519_private.pem
```

---

# 🧠 Philosophie

> **"Security is not optional."**

> **"Strong encryption should be accessible to everyone."**

---

<div align="center">

### 🔐 Built by Oktopus-Motor

Cybersecurity • Secure Development • Cryptography

</div>
