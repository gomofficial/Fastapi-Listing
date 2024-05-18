from uuid import uuid4, UUID
from .engine import Base
from sqlalchemy import (ForeignKey, Column, Table)
from sqlalchemy.orm import relationship,Mapped,mapped_column
from typing import List,Optional

class User(Base):
    __tablename__ = 'users'

    username: Mapped[str]       = mapped_column(unique=True, nullable=False)
    email: Mapped[str]          = mapped_column(unique=True, nullable=False)
    password: Mapped[str]       = mapped_column(nullable=False)
    is_staff: Mapped[bool]      = mapped_column(default=False)
    is_active: Mapped[bool]     = mapped_column(default=False)
    id: Mapped[UUID]            = mapped_column(primary_key=True, default_factory=uuid4)


    def __repr__(self):
        return f"<User {self.username}"   

