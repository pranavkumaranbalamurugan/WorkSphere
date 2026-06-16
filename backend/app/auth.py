#Libraries Import
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt

#Services Import
from app.models import User
from app.schemas import CreateUserRequest, Token
from app.db import get_db
from app.config import SECRET_KEY, ALGORITHM, bcrypt_context


auth = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"



db_dependency= Annotated[Session, Depends(get_db)]

@auth.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):


    create_user_model = User(
        work_email=create_user_request.work_email,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        company_id=create_user_request.company_id
    )

    db.add(create_user_model)
    db.commit()

@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not find user')
    
    token = create_access_token(
        user.work_email, 
        user.role,
        user.company_id,
        timedelta(minutes=20))

    return {'access_token':token, "token_type": 'bearer'}


def authenticate_user(work_email: str, password: str, db):
    user = db.query(User).filter(User.work_email == work_email).first()

    print("User found: ",user)

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(
        work_email: str,
        role:str,
        company_id:str, 
        expires_delta: timedelta
        ):
    
    payload = {
        'work_email': work_email,
        'role': role, 
        'company_id':company_id
        }
    
    expires = datetime.utcnow() + expires_delta
    
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

