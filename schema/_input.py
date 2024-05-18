from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class RegisterInput(BaseModel):
    username:str
    email:str
    password:str

class UpdateUserProfile(BaseModel):
    new_username:str

class AuthenticateUser(BaseModel):
    username:str
    password:str
