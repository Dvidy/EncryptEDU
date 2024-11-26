import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

class Decryptor:
    def __init__(self, extensions):
        self.extensions = extensions
        self.fernet = None

    def load_private_key(self):
        # Načte privátní klíč z environmentální proměnné
        private_key_path = os.getenv("PRIVATE_KEY_PATH")
        if not private_key_path:
            raise ValueError("PRIVATE_KEY_PATH není nastavena jako environmentální proměnná.")

        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None  # Pokud je klíč chráněn heslem, nahraď None heslem
            )
        return private_key

    def load_symmetric_key(self, private_key):
        # Načte a dešifruje symetrický klíč pomocí privátního klíče
        with open("encrypted_sym_key.bin", "rb") as key_file:
            encrypted_symmetric_key = key_file.read()

        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
        )
        self.fernet = Fernet(symmetric_key)

    def decrypt_files(self, directory):
        # Prohledá adresář a dešifruje soubory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as f:
                            encrypted_data = f.read()
                        decrypted_data = self.fernet.decrypt(encrypted_data)
                        with open(file_path, "wb") as f:
                            f.write(decrypted_data)
                        print(f"Dešifrován soubor: {file_path}")
                    except Exception as e:
                        print(f"Chyba při dešifrování {file_path}: {e}")

if __name__ == "__main__":
    print("Tento skript je pouze pro výuku!")
    confirm = input("Opravdu chcete pokračovat? Napište 'ANO': ")
    if confirm == "ANO":
        decryptor = Decryptor(extensions=[
            ".doc", ".docx", ".xls", ".xlsx", ".pdf",
            ".jpg", ".jpeg", ".png", ".zip", ".rar", ".txt"
        ])
        try:
            private_key = decryptor.load_private_key()
            decryptor.load_symmetric_key(private_key)
            decryptor.decrypt_files(os.path.expanduser("~"))
            print("Dešifrování dokončeno.")
        except Exception as e:
            print(f"Chyba: {e}")
    else:
        print("Operace byla zrušena.")