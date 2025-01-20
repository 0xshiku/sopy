from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# To get a random key like this run: openssl rand -hex 32
SECRET_KEY = "b6b801fba5e3deb719a36216c211f5aa187e46a0019b742bf7b18c97bf0a1092"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_enconde = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({"exp": expire})

    enconded_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm=ALGORITHM)

    return enconded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokendData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
