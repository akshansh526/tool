from pydantic import BaseModel
from typing import Union


class AdminCreate(BaseModel):
    # user_id:  int
    first_name: str
    last_name:str
    email:str
    password: str
    phone_no: int
    is_admin:bool
    # is_active:bool
    organisation_name:str

    class Config:
        orm_mode = True


class AdminOut(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class Admin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class Admin_get(BaseModel):
    user_id:int
    
    class Config:
        orm_mode = True



    
