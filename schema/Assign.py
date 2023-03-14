from pydantic import BaseModel,Json,ValidationError,Json
from schema import Upload_images,Project,User
from typing import List,Any,Optional
from schema.User import UserList
from schema.Upload_images import ImagesIn
from schema.Project import Project_get
from sqlalchemy.dialects.postgresql import ARRAY


class AssignIn(BaseModel):
    user_id:int
    project_id:int
    image_id:int
    
    class Config:
        orm_mode = True


class Assign_to(BaseModel):
    user_id:Optional[list[int]] = None
    image_id: Optional[list[int]] = None
    assigned_by:int
    
    
    class Config:
        orm_mode= True

class GetAssignDetails(BaseModel):
    user_id:User.UserList
    image_id:Upload_images.ImagesIn
    assigned_by:User.UserList
    
    class Config:
        orm_mode = True


class Reviewer(BaseModel):
    reviewer_id:List[int]
    user_id:Optional[int]

    class Config:
        orm_mode=True        