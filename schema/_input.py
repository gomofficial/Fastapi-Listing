from pydantic import BaseModel, model_validator
from datetime import datetime, date
from uuid import UUID
from typing import Union, Optional
from utils.enums import *

class RegisterInput(BaseModel):
    username:str
    password:str         
    fullname: Union[str, None] = None       
    email:str
    DoB: Union[date, None] = None
    gender: Union[GenderEnum,None] = GenderEnum.NOT_SPECIFIED

    @classmethod
    def validate_password(cls, values):
        old_pwd, pw1, pw2 = values.get('old_password'), values.get('password_1'), values.get('password_2')
        if len(pw1) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in pw1) or not any(c.islower() for c in pw1):
            raise ValueError("Password must have both uppercase and lowercase letters")


class UpdateUserProfile(BaseModel):
    username:str|None      = None
    fullname:str|None      = None   
    email:str|None         = None
    DoB:date|None          = None
    gender:GenderEnum|None = None



class AuthenticateUser(BaseModel):
    username:str
    password:str

class PasswordChange(BaseModel):
    password_1:str
    password_2:str
    old_password:str

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        old_pwd, pw1, pw2 = values.get('old_password'), values.get('password_1'), values.get('password_2')
        print(values)
        if pw1 != pw2:
            raise ValueError("Passwords should match")
        if len(pw1) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in pw1) or not any(c.islower() for c in pw1):
            raise ValueError("Password must have both uppercase and lowercase letters")
        
        return values


class ListingInput(BaseModel):
    type:TypeEnum
    availableNow:bool|None = None
    address:str


