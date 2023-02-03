from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status
from . import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")


async def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.validUser(data,credentials_exception)

