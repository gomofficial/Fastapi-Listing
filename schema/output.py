from pydantic import BaseModel
from typing import Union
from uuid import UUID
from datetime import datetime
from utils.enums import *
from datetime import date

class UserOutput(BaseModel):
    id:         UUID
    username:   str
    fullname:   Union[str, None]
    email:      str
    DoB:        Union[datetime, None]      
    gender:     GenderEnum          
    createdAt:  datetime         
    updatedAt:  datetime
    
    class Config:
        form_attributes = True

     
class ListingOutput(BaseModel):
    id          : UUID
    type        : TypeEnum
    availableNow: bool
    owner       : str
    address     : str
    createdAt   : datetime
    updatedAt   : datetime