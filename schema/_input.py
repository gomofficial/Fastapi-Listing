from pydantic import BaseModel, model_validator, Field
from datetime import datetime, date
from uuid import UUID
from typing import Union, Optional
from utils.enums import *



class RegisterInput(BaseModel):
    username:str = Field(description="the usename of the user it must be unique")
    password:str = Field(description="the password of user")    
    fullname: Union[str, None] =Field(default=None, description="Example : Rooh Allah Khomeyni")    
    email:str = Field(description="the email of the user it must be unique")
    DoB: Union[date, None] = Field(default=None, description="date of birth")
    gender: Union[GenderEnum,None]  = Field(default=GenderEnum.NOT_SPECIFIED, description="MALE or FEMALE")

    @model_validator(mode='before')
    def validate_password(cls, values):
        pwd = values.get('password')
        if len(pwd) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in pwd) or not any(c.islower() for c in pwd):
            raise ValueError("Password must have both uppercase and lowercase letters")
        return values
    
    @model_validator(mode='before')
    def validate_DoB(cls, values):
        start_date = date(1948, 1, 1)
        end_date = date.today()

        if start_date <= datetime.strptime(values.get("DoB"), '%Y-%m-%d').date() <= end_date:
            return values
        else:
            raise ValueError("Invalid Birth Date")




class UpdateUserProfile(BaseModel):
    username:str|None      = Field(default=None, description="the usename of the user it must be unique")
    fullname:str|None      = Field(default=None, description="Example : Rooh Allah Khomeyni")
    email:str|None         = Field(default=None, description="the email of the user it must be unique")
    DoB:date|None          = Field(default=None, description="date of birth")
    gender:GenderEnum|None = Field(default=None, description="MALE or FEMALE")



class AuthenticateUser(BaseModel):
    username:str = Field(description="the usename of the user it must be unique")
    password:str = Field(description="the password of user")    



class PasswordChange(BaseModel):
    password_1:str  = Field(description="new password")    
    password_2:str = Field(description="confirm new password")    
    old_password:str = Field(description="old password")    

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
    type:TypeEnum  = Field(description="HOUSE or APARTMENT")    
    availableNow:bool|None = Field(default=None, description="true or false")    
    address:str = Field(description="address of the building")    


