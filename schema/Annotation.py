from pydantic import BaseModel
from typing import Optional,List,Dict,Union
from schema import Project,Classes,User,Upload_images

from sqlalchemy.ext.declarative import DeclarativeMeta
import json



class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class Annotation_in(BaseModel):
    
    bounding_box:Dict

    class Config:
        orm_mode = True


# class ClassCoord(BaseModel):
    
class Object(BaseModel):
    class_name: str
    coord: List[float]
# class_coord:ClassCoord
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
    bounding_boxes:Union[dict] = None

    class Connfig:
        orm_mode= True        



# c = Object()
# print (json.dumps(c, cls=AlchemyEncoder))





# json_str = """
# {
#     "class_coord":
# 	[
# 		{"class_name" : "car" , "coord":[121.12, 79.123,  456.123, 44.11]},
# 		{"class_name" : "car" , "coord":[121.12, 79.123,  456.123, 44.11]},
# 		{"class_name" : "car" , "coord":[121.12, 79.123,  456.123, 44.11]}
# 	]
# }
# """

# obj = Object.parse_raw(json_str)
# print(obj)
