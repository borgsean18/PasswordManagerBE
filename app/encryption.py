from cryptography.fernet import Fernet, InvalidToken
import os
import logging

# Generate or load a key for encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key()
    os.environ["ENCRYPTION_KEY"] = str(ENCRYPTION_KEY)

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return fernet.encrypt(data).decode()

def decrypt_data(encrypted_data: str | bytes) -> str:
    try:
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        elif not isinstance(encrypted_data, bytes):
            raise ValueError(f"Expected str or bytes, got {type(encrypted_data)}")
        
        decrypted = fernet.decrypt(encrypted_data)
        return decrypted.decode()
    except InvalidToken as e:
        logging.error(f"Invalid token error: {str(e)}")
        logging.error("This likely means the encryption key is incorrect or the data is corrupted.")
        raise
    except Exception as e:
        logging.error(f"Decryption error: {str(e)}") # Log first 20 chars or bytes
        raise