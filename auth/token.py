import time
import os

from jose import JWTError, jwt

from schemas.user import TokenData





def create_access_token(data: dict):
    payload = {
        "userID": data,
        "expiry": time.time() + 20000
    }
    
    encoded_jwt = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def validUser(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("userID")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception
    