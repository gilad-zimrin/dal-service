from enum import Enum
from os import getenv

from jwt import encode, decode, PyJWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.exception_handlers import logger

SECRET_KEY =  getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.1
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class Role(Enum):
    admin = 'Admin'
    customer = 'Customer'
    company = 'Company'

class TokenData(BaseModel):
    username: str | None = None
    role: Role | None = None
    exp: datetime | None = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Returns True if matched, else False
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a str - the password field
    :param password:
    :return:
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    to_encode.update({'role': to_encode['role'].value})
    if to_encode['role'] != Role.admin.value:
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username, role=payload.get("role"))
    except ExpiredSignatureError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token had expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    except PyJWTError:
        logger.exception("An error has occurred decoding token")
        raise credentials_exception


def require_role(required_role: Role):
    """
    Factory function that returns a dependency checking for a specific role.
    """

    async def check_user_role(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if required_role != current_user.role and current_user.role != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"{required_role} privileges required")
        return current_user

    return check_user_role

