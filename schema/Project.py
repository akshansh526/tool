from pydantic import BaseModel
import datetime
from typing import List,Optional,Union

class Project_create(BaseModel):
    # project_id:  int
    project_name: str
    description:str
    industries_name:str
    start_date:str
    enddate:Optional[str]=None
    class_name:Optional[List]=None
    approved_by:Optional[str] = None
    

    class Config:
        orm_mode = True



class Update_name(BaseModel):
      class_name:str
      class Config:
          orm_mode=True

class Project_get(BaseModel):
    project_id:int
    project_name:str
    project_path:str
           
    class Config:
        orm_mode = True    
class Project_path(BaseModel):
    project_path:str
    
    class Config:
        orm_mode = True  
class Edit_project(BaseModel):
    project_name:Optional[str] = None
    project_path:Optional[str]=None
    approved_by:Optional[str]=None
    industries_name:Optional[str]=None
    description:Optional[str]=None
    
    
    class Config:
        orm_mode=True



class Project_update(BaseModel):
    project_id:int
    project_name:str
    description:str
    indsutries_id:int
    assigned_to:str
    no_of_classes:int
    # start_date:datetime.date
    # modified_date:datetime.date
    
    class Config:
        orm_mode = True  


class ProjectFilter(BaseModel):
    start_date:Optional[datetime.date]=None
    user_id:Union[int, None]=None
    project_id:Union[int, None]=None
    project_name:Union[str, None]=None
    class Config:
        orm_mode= True


class ProjectUserBasis(BaseModel):
    user_id:int
    project: List[Project_get]
    class Config:
        orm_mode= True

class Project_user(BaseModel):
    user_id:int
    project_id:int
    image_id:int
    class  Config:
        orm_mode=True
