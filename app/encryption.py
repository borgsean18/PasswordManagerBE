from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import logging
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Generate or load a key for encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key()
    os.environ["ENCRYPTION_KEY"] = ENCRYPTION_KEY.decode()
    logger.info(f"Generated new encryption key: {ENCRYPTION_KEY}")

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str | bytes) -> str:
    logger.info(f"ENCRYPTION_KEY: {os.getenv('ENCRYPTION_KEY')}")
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

def deterministic_encrypt_data(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    
    # Use a fixed IV (16 bytes of zeros)
    iv = b'\x00' * 16
    
    # Use AES-CBC mode with the fixed IV
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY[:32]), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the data to be a multiple of 16 bytes
    padded_data = data + b'\0' * (16 - len(data) % 16)
    
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encode the result as base64
    return base64.b64encode(encrypted_data).decode()

def deterministic_decrypt_data(encrypted_data: str | bytes) -> str:
    try:
        if isinstance(encrypted_data, str):
            encrypted_data = base64.b64decode(encrypted_data)
        elif not isinstance(encrypted_data, bytes):
            raise ValueError(f"Expected str or bytes, got {type(encrypted_data)}")
        
        # Use a fixed IV (16 bytes of zeros)
        iv = b'\x00' * 16
        
        # Use AES-CBC mode with the fixed IV
        cipher = Cipher(algorithms.AES(ENCRYPTION_KEY[:32]), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove padding
        return decrypted_data.rstrip(b'\0').decode()
    except Exception as e:
        logging.error(f"Decryption error: {str(e)}")
        raise