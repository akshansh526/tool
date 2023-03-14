from pydantic import BaseModel


class Industries(BaseModel):
    # industries_id:int
    industry_name:str
    industry_description:str
    class Config:
        orm_mode = True



class Industries_get(BaseModel):
    
    industries_id:int
    industries_name:str
    class Config:
        orm_mode = True