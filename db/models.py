from uuid import uuid4
from .engine import Base
from sqlalchemy import (UUID, ForeignKey, Column, Table, String, Boolean, DateTime, Enum)
from sqlalchemy.orm import relationship,Mapped,mapped_column
from typing import List,Optional
from sqlalchemy.sql import func


class GenderEnum(Enum):
    FEMALE = "FEMALE"
    MALE = "MALE"
    NOT_SPECIFIED = "NOT_SPECIFIED"

class TypeEnum(Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"


class User(Base):
    __tablename__ = 'users'
    
    id                   = Column(UUID, primary_key=True, default=uuid4)
    username             = Column(String, unique=True, nullable=False)
    fullname             = Column(String, unique=False, nullable=True, default=None)
    email                = Column(String, unique=True, nullable=False)
    hashed_password      = Column(String, nullable=False)
    DoB                  = Column(DateTime, nullable=True, default=None)
    gender               = Column(GenderEnum, default=GenderEnum.NOT_SPECIFIED)
    createdAt            = Column(DateTime, default=func.now())
    updatedAt            = Column(DateTime, default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"<User {self.username}"   


class Listing(Base):
    __tablename__ = 'listings'

    id                   = Column(UUID, primary_key=True, default=uuid4)
    type                 = Column(TypeEnum, nullable=False)
    availableNow         = Column(Boolean, default = True)

    ownerId              = Column(UUID, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner                = relationship("User")

    address              = Column(String, nullable=False)
    createdAt            = Column(DateTime, default=func.now())
    updatedAt            = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<{self.owner.username} : {self.address}"

