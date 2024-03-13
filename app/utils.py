from passlib.context import CryptContext
# Imports for creating access and refresh tokens
import os
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRATION_MINUTES = 30  # 30 MIN
REFRESH_TOKEN_EXPIRATION_MINUTES = 60 * 24 * 7  # 7 DAYS
ALGORITHM = 'HS256'
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']  # KEEP SECRET
JWT_REFRESH_SECREET_KEY = os.environ['JWT_REFRESH_SECREET_KEY']  # KEEP SECRET


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)

    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,ALGORITHM)
    print('ENCODED_JWT: '+encoded_jwt)
    return encoded_jwt
