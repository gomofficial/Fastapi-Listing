from uuid import uuid4
from .engine import Base
from sqlalchemy import (UUID, ForeignKey, Column, String, Boolean, Date, Enum, TIMESTAMP)
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy.sql import func
import datetime

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
    DoB                  = Column(Date, nullable=True, default=None)
    gender               = Column(String, default=GenderEnum.NOT_SPECIFIED)
    createdAt            = Column(TIMESTAMP, default=datetime.datetime.now())
    updatedAt            = Column(TIMESTAMP, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    listings = relationship('Listing', back_populates='owner', lazy='subquery')

    def __repr__(self):
        return f"<User {self.username}>"   


class Listing(Base):
    __tablename__ = 'listings'

    id                   = Column(UUID, primary_key=True, default=uuid4)
    type                 = Column(String, nullable=False)
    availableNow         = Column(Boolean, default = True)
    ownerId              = Column(UUID, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner                = relationship("User", back_populates='listings', lazy='subquery')
    address              = Column(String, nullable=False)
    createdAt            = Column(TIMESTAMP, default=func.now())
    updatedAt            = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<{self.owner.username} : {self.address}"

 