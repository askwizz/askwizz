import logging
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from esearch.api.exceptions import NotAuthenticatedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "RS256"
SECRET_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAphHk9gRs7hlL/s/wmjfw
9iYkAEPDf2TjKf9LQ3zFOgWLhy+Db2JVO85XpHHPAB0FNyvqEMRZH/dFgZiGD7JB
R9xc1WOa1/MbVajRbKyqHg8AX6zz7j9GSnWk1ptnmr0kE0emu46zhJEg2Hu6fusU
GH8+JuVILwrXX/bNvZocaiQksN/LQJRL4nkl3mtehxKCid0+MeUyRvh01rxoDc0s
whAbSjoqAn5T1QuqpKSOiSlhrKtZXv7iFKmQ/Ra2tY5XM9a6XwLoD3YQ+wbP0PaQ
PkQ2EHlxCXfg9qF60w+tfQW9ak5xYyYShhIwt4BZwKi7ldBfRsjAGEzo3gjBDB6/
DQIDAQAB
-----END PUBLIC KEY-----
"""


class UserData(BaseModel):
    user_id: str


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserData:
    override_clerk = os.getenv("API_OVERRIDE_CLERK")
    if override_clerk == "true":
        return UserData(user_id="user_2Qklbs5sgdrrPJhZ8g1KtlfRmkH")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # type: ignore
        if user_id is None:
            raise credentials_exception  # noqa: TRY301
        token_data = UserData(user_id=user_id)
    except JWTError:
        logging.exception("Error occured while decoding JWT token")
        raise credentials_exception
    return token_data


def is_authenticated(user_data: UserData) -> bool:
    return user_data.user_id is not None


def throw_if_not_authenticated(user_data: UserData) -> None:
    if not is_authenticated(user_data):
        raise NotAuthenticatedException()
