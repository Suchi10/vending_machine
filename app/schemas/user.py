from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    deposit: float
    role: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    ...


class UserUpdate(BaseModel):
    deposit: float
    role: str
