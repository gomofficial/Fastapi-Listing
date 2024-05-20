from  fastapi import APIRouter, Body, Depends
from  schema._input import *
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.users import UsersOperation
from schema import jwt
from utils.auth import JWTHandler
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.utils import successful_login_notification
from utils import rate_limit_user
from fastapi import Request

user_router = APIRouter()

 
@user_router.post('/register')
async def register( db_session: Annotated[AsyncSession, Depends(get_db)],
                    data: RegisterInput = Body()):
    
    user = await UsersOperation(db_session).create(data.model_dump())
    
    return user


@user_router.get("/profile")
async def get_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],
                           token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    uesr_profile = await UsersOperation(db_session).get_user_profile(token_data.username)

    return uesr_profile


@user_router.put("/update")
async def update_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],
                              data:UpdateUserProfile = Body(),
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    
    user = await UsersOperation(db_session).update(token_data.username, data.model_dump(exclude_none=True))

    return user

@user_router.put("/change_password")
async def update_user_password(db_session: Annotated[AsyncSession, Depends(get_db)],
                              data:PasswordChange = Body(),
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    
    user = await UsersOperation(db_session).update_password(token_data.username, data.model_dump())

    return user


@user_router.delete("/delete")
async def user_delete_account(db_session: Annotated[AsyncSession, Depends(get_db)],
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    await UsersOperation(db_session).user_delete_account(token_data.username)


@user_router.post("/token")
async def authenticate(db_session: Annotated[AsyncSession, Depends(get_db)],
                       form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       dependencies = Depends(rate_limit_user)):
    token = await UsersOperation(db_session).login(form_data.username,form_data.password)
    successful_login_notification(form_data.username)
    return token