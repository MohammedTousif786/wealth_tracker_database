from jose import jwt
from fastapi import HTTPException

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def create_token(data: dict):

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
