from pydantic import BaseModel
from typing import Union,Optional,List
from schema.Roles import RolesName 
from uuid import UUID
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
 
    first_name: str
    last_name:str
    email:str
    password: str
    phone_no: int
    organisation_name:str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    email: str
    password: str
 

    class Config:
        orm_mode = True

class UserList(BaseModel):
 
    first_name: str 
    last_name:str
    email:str 
    roles_id:List[RolesName]
    password: str 
    phone_no: int 
    organisation_name:str

    class Config:
        orm_mode = True

class User(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class User_get(BaseModel):
    user_id:int
    first_name:str
    class Config:
        orm_mode = True


class User_map(BaseModel):

    first_name:Optional[str]=None
    
    class Config:
        orm_mode= True




class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
