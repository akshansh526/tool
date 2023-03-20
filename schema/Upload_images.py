from pydantic import BaseModel
from typing import List,Optional
import datetime

class ImagesIn(BaseModel):
    image_url: str
    user_id:int
    project_id:int
    dateCreated:datetime.date
    class Config:
        orm_mode = True

class Rename_image(BaseModel):
    image_name:Optional[str] = None
    image_url:Optional[str] = None
    class Config:
        orm_mode = True
    
class ImageOut(ImagesIn):
    image_id:int
    image_url: str

    class Config:
        orm_mode = True