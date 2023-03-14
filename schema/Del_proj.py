from pydantic import BaseModel



class Project_del(BaseModel):
    project_id:int
    project_name:str
    
           
    class Config:
        orm_mode = True  