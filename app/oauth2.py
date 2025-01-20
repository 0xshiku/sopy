from jose import JWTError, jwt
from datetime import datetime, timedelta

# To get a random key like this run: openssl rand -hex 32
SECRET_KEY = "b6b801fba5e3deb719a36216c211f5aa187e46a0019b742bf7b18c97bf0a1092"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_enconde = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"exp": expire})

    enconded_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm=ALGORITHM)

    return enconded_jwt
