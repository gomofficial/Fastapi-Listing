from  fastapi import APIRouter, Body, Depends
from  schema._input import *
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.users import UsersOperation
from schema import jwt
from utils.auth import JWTHandler

user_router = APIRouter()


@user_router.post('/register')
async def register( db_session: Annotated[AsyncSession, Depends(get_db)],
                    data: RegisterInput = Body()):
    
    user = await UsersOperation(db_session).create(
        data.username,
        data.email,
        data.password
        )
    
    return user


@user_router.get("/{username}",)
async def get_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],
                           username: str):
    uesr_profile = await UsersOperation(db_session).get_user_by_username(username)

    return uesr_profile


@user_router.put("/")
async def update_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],
                              data:UpdateUserProfile = Body(),
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    
    user = await UsersOperation(db_session).update_username(
        token_data.username, data.new_username)

    return user


@user_router.delete("/")
async def user_delete_account(db_session: Annotated[AsyncSession, Depends(get_db)],
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    await UsersOperation(db_session).user_delete_account(token_data.username)


@user_router.post("/login")
async def authenticate(db_session: Annotated[AsyncSession, Depends(get_db)],
                              data:AuthenticateUser = Body()):
    token = await UsersOperation(db_session).login(data.username,data.password)
    return token