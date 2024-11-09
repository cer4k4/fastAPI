from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserCreate(UserBase):
    password: str = Field(min_length=8)




class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError('At least one field must be provided for update')
        return values

class UserResponse(UserBase):
    id: str
    disabled: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        populate_by_name = True