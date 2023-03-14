from pydantic import BaseModel
from typing import Optional,List,Dict
from schema import Project,Classes,User,Upload_images



class Annotation_in(BaseModel):
    
    bounding_box:Dict

    class Config:
        orm_mode = True

class GetAnnotation(BaseModel):
    image_annotation_mapping_id:int
    image_id:int
    class_id:int
    user_id:int
    project_id:int


    class Config:
        orm_mode = True


class AnnotOut(BaseModel):
    image_annotation_id:int
    details:Annotation_in
    
    class Config:
        orm_mode = True



class Update_bounding_boxes(BaseModel):
    bounding_boxes:Optional[dict] = None

    class Connfig:
        orm_mode= True        