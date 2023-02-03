from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from schemas.user import User
from db.engine import db
from auth.hashing import Hasher
from auth.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(tags=["User"])


@user_router.post("/user/signup/")
def user_signup(request: User):
    user = db.users.find_one({"email":request.email})
    if not user:
        data = {
            "first_name":request.first_name,
            "last_name": request.last_name,
            "email": request.email,
            "password": Hasher.get_password_hash(request.password)
        }
        db.users.insert_one(data)
        access_token = create_access_token(request.email)
        return JSONResponse(content={"access_token":access_token}, status_code=201)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with same email is already register")


@user_router.post("/user/login/")
async def login_user(request: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"email":request.username})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    
    elif not Hasher.verify_password(request.password,user['password']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User or Password is not valid")

    access_token = create_access_token(request.username)
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)
