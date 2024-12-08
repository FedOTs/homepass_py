from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import get_auth_data
from app.users.dao import UsersDAO

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=366)
    to_encode.update({"exp":expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

def get_password_hash(password:str) -> str:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    return pwd_context.verify(plain_pass, hashed_pass)

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or verify_password(plain_pass=password, hashed_pass=user.hashed_password) is False:
        return None
    return user


