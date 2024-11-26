# Šifrování a Dešifrování (Simulace ransomware)

## Účel projektu
Tento repozitář obsahuje skripty pro simulaci šifrování (ransomware) a následného dešifrování. Projekt je určen **pouze pro vzdělávací účely**, aby pomohl lidem pochopit principy ransomwaru.

---

## Jak to funguje
-**`Ecrypt.py`**: Šifruje soubory ve složce uživatele (home directory). K šifrování symetrického klíče vyžaduje veřejný RSA klíč.
- **`Decrypt.py`**: Dešifruje soubory zašifrované pomocí `Encrypt.py`. K dešifrování symetrického klíče vyžaduje privátní RSA klíč.

Skripty pracují s těmito typy souborů: `.doc`, `.pdf`, `.jpg`, `.txt` a další. Typy souborů lze upravit v proměnné `extensions`.

---

## DŮLEŽITÉ UPOZORNĚNÍ
**Tento kód by měl být spuštěn pouze ve virtuálním počítači (VirtualBox, VMware, apod.), který nemá přístup k reálným datům nebo síti.**
Použití mimo bezpečné prostředí může vést k nechtěnému šifrování důležitých souborů a ztrátě dat.

---

## Nastavení 
1. Naklonujte repozitář:
   ```bash
    git clone <url-repozitáře>

2. Nainstalujte potřebné knihovny:
   ```bash
    pip install cryptography

3. RSA klíče:
  Vygenerujte privátní klíč:
    ```bash
    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

  Z privátního klíče vytvořte veřejný klíč:
  
    openssl rsa -pubout -in private_key.pem -out public_key.pem

4. Nastavte environmentální proměnné:
  Pro šifrování:
   ```bash
    export PUBLIC_KEY_PATH=/cesta/k/public_key.pem
  
  Pro dešifrování:
  
    export PRIVATE_KEY_PATH=/cesta/k/private_key.pem
    
---

# Použití

Šifrování souborů
    Spusťte následující příkaz pro šifrování souborů:

    python Encrypt.py

Dešifrování souborů
Spusťte následující příkaz pro dešifrování souborů:

    python Decrpyt.py

---

# Upozornění
- Tento kód je určen pouze pro vzdělávací účely. Jakékoli zneužití tohoto softwaru je nelegální a neetické.
* Důrazně doporučujeme používat tento kód pouze ve virtuálním prostředí bez přístupu k reálným datům.
+ Autor nenese odpovědnost za nesprávné použití těchto skriptů.

