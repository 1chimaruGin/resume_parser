from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.enums import RoleType


# Shared properties
class UserBase(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    role: Optional[RoleType] = None
    full_name: Optional[str] = None
    organization: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_name: str
    password: str
    email: Optional[EmailStr] = None
    role: Optional[RoleType] = "user"
    organization: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


# class UserGroupBase(BaseModel):
#     org: Optional[str] = None
#     user_id: Optional[int] = None

# class UserGroupCreate(UserGroupBase):
#     org: str
#     user_id: int

# class UserGroup(UserGroupBase):
#     id: Optional[int] = None

#     class Config:
#         orm_mode = True

# class UserGroupInDB(UserGroupBase):
#     pass
