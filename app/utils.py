from cryptography.fernet import Fernet
from app.config import get_pw_key
from itsdangerous import URLSafeTimedSerializer

cipher = Fernet(get_pw_key())

def encrypt(secret: str):
    encrypted = cipher.encrypt(secret.encode()).decode()
    return encrypted


def decrypt(secret: str):
    decrypted = cipher.decrypt(secret.encode()).decode()
    return decrypted

serializer = URLSafeTimedSerializer(secret_key=get_pw_key(), salt="homepass_email-configuration")

def create_url_safe_token(data:dict):
    token = serializer.dumps(data, salt="homepass_email-configuration")
    return token

def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)
        return {"message":"ok", "token_data":token_data}
    except Exception as e:
        return {"message":str(e), "token_data":None}

