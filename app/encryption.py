from cryptography.fernet import Fernet
import os

# Generate or load a key for encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key()

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return fernet.decrypt(encrypted_data.encode()).decode()