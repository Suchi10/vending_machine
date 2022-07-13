import enum
from typing import Optional

from sqlalchemy import Enum
from sqlmodel import Field, SQLModel


class UserRole(str, enum.Enum):
    SELLER = "seller"
    BUYER = "buyer"


class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False, index=True
    )
    username: str = Field(index=False, nullable=False)
    password: str = Field(index=False, nullable=False)
    deposit: float = Field(nullable=False, index=False)
    role: str = Field(Enum(UserRole), nullable=False, index=False)
