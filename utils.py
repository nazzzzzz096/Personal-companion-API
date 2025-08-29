# app/utils.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """for converting the password to encrypted form"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """used to verify the password the plain one and the hashed one"""
    return pwd_context.verify(plain_password, hashed_password)
