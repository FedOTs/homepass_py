from cryptography.fernet import Fernet
from app.config import get_pw_key

cipher = Fernet(get_pw_key())


def encrypt(secret: str):
    encrypted = cipher.encrypt(secret.encode()).decode()
    return encrypted


def decrypt(secret: str):
    decrypted = cipher.decrypt(secret.encode()).decode()
    return decrypted