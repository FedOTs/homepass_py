from cryptography.fernet import Fernet

def generate_key():
    print(Fernet.generate_key().decode())

generate_key()