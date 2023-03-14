from pydantic import BaseModel


class Create_roles(BaseModel):
    roles_name:str
    roles_description:str
    class Config:
        orm_mode=True


class Get_roles(BaseModel):
    roles_name:str
    roles_description:str
    class Config:
        orm_mode=True


class RolesName(BaseModel):
    roles_name:str
    
    class Config:
        orm_mode=True

class Assign_roles(BaseModel):
    roles_id:int
                