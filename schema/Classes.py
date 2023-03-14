from pydantic import BaseModel
from typing import List, Union,Optional
from schema.Project import Project_get



class Add_classes(BaseModel):

    
    class_name: Optional[list[str]] = None

    
    
    class Config:
       orm_mode = True  

class Classes_get(BaseModel):
    class_id:int
    class_name:str
    project_id:List[Project_get]
    
    class Config:
        orm_mode = True  

