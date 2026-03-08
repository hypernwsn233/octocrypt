<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=240&color=0:000000,50:0f172a,100:00ff88&text=OctoCrypt&fontSize=58&fontColor=00ff88&animation=fadeIn&fontAlignY=38&desc=Advanced%20File%20Encryption%20Platform&descAlignY=60&descColor=7CFFB2" />

# 🐙 OctoCrypt

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&pause=900&color=00FF88&center=true&vCenter=true&width=1000&lines=Milit%C3%A4risch+inspirierte+Dateiverschl%C3%BCsselung;AES-256-GCM+%7C+Ed25519+%7C+Secure+Compression;CLI+und+GUI+f%C3%BCr+moderne+Sicherheits-Workflows;Built+for+developers%2C+researchers+and+security+enthusiasts" alt="Typing SVG" />

<br>

<img src="https://img.shields.io/badge/Encryption-AES--256--GCM-000000?style=for-the-badge&logo=letsencrypt&logoColor=00ff88" />
<img src="https://img.shields.io/badge/Signature-Ed25519-000000?style=for-the-badge&logo=protocolsdotio&logoColor=00ff88" />
<img src="https://img.shields.io/badge/Compression-zlib-000000?style=for-the-badge&logo=gzip&logoColor=00ff88" />
<img src="https://img.shields.io/badge/Language-Python%203.10+-000000?style=for-the-badge&logo=python&logoColor=00ff88" />
<img src="https://img.shields.io/badge/Interface-CLI%20%2B%20GUI-000000?style=for-the-badge&logo=gnometerminal&logoColor=00ff88" />

</div>

---

## `> init project`

**OctoCrypt** ist ein modernes Sicherheitswerkzeug zur **Verschlüsselung sensibler Dateien** mit einem Fokus auf:

- **starke authentifizierte Verschlüsselung**
- **digitale Signaturen**
- **Integritätsschutz**
- **sichere Passwortverarbeitung**
- **kompakte Speicherung durch Kompression**

Das Ziel: ein Tool, das sich **wie ein professionelles Security-Projekt** anfühlt und gleichzeitig **klar, praktisch und robust** bleibt.

---

## `> core features`

```txt
[✓] AES-256-GCM Datei-Verschlüsselung
[✓] Sichere Passwortvalidierung
[✓] Ed25519 digitale Signaturen
[✓] zlib-Kompression
[✓] CLI für schnelle Workflows
[✓] GUI für komfortable Nutzung
[✓] Integritäts- und Manipulationsschutz
[✓] Eigenes .octo Containerformat
````

---

## `> security architecture`

<div align="center">

```mermaid
flowchart LR
    A[Originaldatei] --> B[zlib Kompression]
    B --> C[AES-256-GCM Verschlüsselung]
    C --> D[.octo Container]
    D --> E[Metadaten]
    E --> F[Ed25519 Signatur]
```

</div>

---

## `> tech stack`

<div align="center">

<img src="https://skillicons.dev/icons?i=python,git,github,linux" />

</div>

```txt
Cryptography: AES-256-GCM
Signing:      Ed25519
Compression:  zlib
GUI:          Tkinter
Runtime:      Python 3.10+
```

---

## `> installation`

```bash
git clone https://github.com/hypernwsn233/octocrypt.git
cd octocrypt
pip install -r requirements.txt
```

---

## `> usage`

### Datei verschlüsseln

```bash
python octocrypt.py encrypt secret.txt

password: ********
confirm password: ********

file encrypted -> secret.octo
```

### Datei entschlüsseln

```bash
python octocrypt.py decrypt secret.octo

password: ********

file decrypted -> secret.txt
```

### Signaturschlüssel generieren

```bash
python octocrypt.py keygen
```

### GUI starten

```bash
python octocrypt.py gui
```

---

## `> real cli style`

```bash
octocrypt encrypt secret.txt
password: ********
file encrypted -> secret.octo
```

Für Windows kann `octocrypt.bat` verwendet werden, um denselben Workflow bereitzustellen.

---

## `> project structure`

```bash
octocrypt/
│
├── octocrypt.py
├── requirements.txt
├── octocrypt.bat
├── README.md

```

---

## `> .octo file format`

Das `.octo`-Format wurde so entworfen, dass es **strukturiert, prüfbar und erweiterbar** bleibt.

```txt
+--------------------------------------------------+
| HEADER                                           |
| Version / Magic Bytes                            |
+--------------------------------------------------+
| METADATA                                         |
| Algorithmus, Salt, Nonce, Hash, Signatur         |
+--------------------------------------------------+
| CIPHERTEXT                                       |
| AES-256-GCM verschlüsselte Nutzdaten             |
+--------------------------------------------------+
```

---

## `> why aes-256-gcm`

**AES-256-GCM** bietet:

* starke symmetrische Verschlüsselung
* Authentifizierung der Daten
* Erkennung von Manipulation
* hohe Praxistauglichkeit
* moderne Standard-Sicherheit

---

## `> why ed25519`

**Ed25519** wird verwendet für:

* schnelle digitale Signaturen
* starke Integritätsprüfung
* moderne Sicherheitsstandards
* klare Trennung zwischen Verschlüsselung und Signatur

---

## `> security notes`

```txt
[!] Niemals Passwörter über --password oder Klartext-Parameter übergeben
[!] Private Schlüssel nur auf vertrauenswürdigen Systemen speichern
[!] Schlüssel regelmäßig sichern
[!] Signaturprüfung beim Decrypt aktiviert lassen
[!] Produktionsdaten nur mit sicheren Backup-Strategien verschlüsseln
```

Standardpfad für den privaten Schlüssel:

```bash
~/.octocrypt/ed25519_private.pem
```

---

## `> design philosophy`

> **"Encryption should be strong, clean and practical."**

> **"Security is not a feature. It is the foundation."**

> **"If data matters, protection must be deliberate."**

---

## `> possible future upgrades`

```txt
[ ] Drag & Drop GUI
[ ] Multi-file encryption
[ ] Directory packaging
[ ] Hardware-key support
[ ] Secure key vault integration
[ ] Argon2-based KDF
[ ] Dark terminal-themed GUI
[ ] Signed release builds
```

---

## `> status`

<div align="center">

<img src="https://img.shields.io/badge/Status-Active%20Development-000000?style=for-the-badge&logo=githubactions&logoColor=00ff88" />
<img src="https://img.shields.io/badge/Security-High%20Priority-000000?style=for-the-badge&logo=securityscorecard&logoColor=00ff88" />
<img src="https://img.shields.io/badge/Focus-Cryptography-000000?style=for-the-badge&logo=databricks&logoColor=00ff88" />

</div>

---

## `> terminal preview`

```bash
┌──(octocrypt㉿secure-node)-[~/projects/octocrypt]
└─$ python octocrypt.py encrypt classified.pdf

[INFO] Loading file...
[INFO] Applying compression...
[INFO] Generating salt and nonce...
[INFO] Encrypting with AES-256-GCM...
[INFO] Signing metadata with Ed25519...
[SUCCESS] Output written to classified.octo
```

---

## `> author`

<div align="center">

# Oktopus-Motor

**Cybersecurity • Secure Software • Full-Stack Engineering**

<img src="https://img.shields.io/badge/Built%20by-Oktopus--Motor-000000?style=for-the-badge&logo=github&logoColor=00ff88" />

</div>

---

<div align="center">

## Zugriff erkannt. README erfolgreich geladen.

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=140&section=footer&color=0:00ff88,50:0f172a,100:000000" />

</div>
```

Se você quiser, eu posso fazer agora uma **versão 2 ainda mais brutal**, com tema **black + neon green + red alert**, parecendo interface de invasão real.
