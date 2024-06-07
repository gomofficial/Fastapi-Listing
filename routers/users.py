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
from schema.jwt import JWTResponsePayload
from utils.redis_utils import *

user_router = APIRouter()

 
@user_router.post('/register')
async def register( db_session: Annotated[AsyncSession, Depends(get_db)],
                    data: RegisterInput = Body()):
    '''
        description : creating a user profile \n
        id : UUID "id of the listing" \n
        body : \n
            username : username most be unique \n
            fullname : firstname and lastname \n          
            email : email \n
            password : should have 8 characters or more and uppercase and lowercase \n
            gender : FEMALE or MALE \n
            DoB : date of birth Example(2024-05-21)
        output :\n
            user
    '''
    user = await UsersOperation(db_session).create(data.model_dump())
    
    return user


@user_router.get("/profile")
async def get_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],
                           token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    '''
        description : authenticated user can get his own profile \n
        body : \n
            None
        output :\n
            user
    '''
    uesr_profile = await UsersOperation(db_session).get_user_profile(token_data.username)

    return uesr_profile


@user_router.put("/update")
async def update_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],
                              data:UpdateUserProfile = Body(),
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    '''
        description : updating user profile \n
        id : UUID "id of the listing" \n
        body : \n
            username : username most be unique \n
            fullname : firstname and lastname \n          
            email : email \n
            password : should have 8 characters or more and uppercase and lowercase \n
            gender : FEMALE or MALE \n
            DoB : date of birth Example(2024-05-21)
        output :\n
            user
    '''
    
    user = await UsersOperation(db_session).update(token_data.username, data.model_dump(exclude_none=True))

    return user

@user_router.put("/change_password")
async def update_user_password(db_session: Annotated[AsyncSession, Depends(get_db)],
                              data:PasswordChange = Body(),
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token),):
    '''
        description : change password \n
        id : UUID "id of the listing" \n
        body : \n
            password1 :new password should have 8 characters or more and uppercase and lowercase \n
            password2 :confirming the new password should have 8 characters or more and uppercase and lowercase \n
            old_password :previous password should have 8 characters or more and uppercase and lowercase \n
        output :\n
            user
    '''
    user = await UsersOperation(db_session).update_password(token_data.username, data.model_dump())

    return user


@user_router.delete("/delete")
async def user_delete_account(db_session: Annotated[AsyncSession, Depends(get_db)],
                              token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    '''
        description : delete account \n
        body : \n
            None
        output :\n
            None
    '''
    await UsersOperation(db_session).user_delete_account(token_data.username)


@user_router.post("/token")
async def authenticate(request: Request,
                       db_session: Annotated[AsyncSession, Depends(get_db)],
                       form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       dependencies = Depends(rate_limit_user)):
    '''
        description : delete account \n
        body : \n
            username : user account username
            password : user account password
        output :\n
            access token
    '''
    token = await UsersOperation(db_session).login(form_data.username,form_data.password)
    payload = JWTResponsePayload(access_token=token)
    await set_device_token(token,form_data.username)
    await set_device_ip(request)
    successful_login_notification(form_data.username)
    return payload

@user_router.post("/logout")
async def logout(request: Request,
                db_session: Annotated[AsyncSession, Depends(get_db)],
                token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token),):
    '''
        description :\n
            logout view \n
        output :\n
            access token
    '''

    await delete_key(token_data.username)
    await delete_ip(request)
    return {"message" : "logout successfully"}