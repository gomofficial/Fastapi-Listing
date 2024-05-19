from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from utils.enums import *

class UserOutput(BaseModel):
    id:         UUID
    username:   str
    fullname:   str
    email:      str
    DoB:        datetime
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