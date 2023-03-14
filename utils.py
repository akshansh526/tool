import os
import shutil
from typing import TypeVar, Type

from pydantic import BaseModel
from sqlalchemy.orm import Query


def upload_images(image_url):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",image_url)
    upload_dir = 'E:/annotation/ai-annotation-backend/Project_datasets/thermal/'
   

    # images_name= image_url.split('/')[-1]
    # filename= os.path.join(upload_dir, images_name)
    # print(filename)

    shutil.copy(image_url, upload_dir)
    return upload_dir

def upload_image(image_url:str):

    upload_dir= 'E:\\tools\\ai-annotation-backend\\Project_datasets'

    image_name= image_url.split('/')[-1]
    print(image_name)
    filename= os.path.join(upload_dir, image_name)
    print(filename)
    print(f"video_url received in api: {image_url}. image to be saved at: {filename}")
    shutil.copy(image_url, filename)
    return filename





class CustomQuery(Query):
    def filter_if(self: Query, condition: bool, *criterion):
        if condition:
            return self.filter(*criterion)
        else:
            return self

    def join_if(self: Query, target:str, condition: bool, *criterion):
        if condition:
            return self.join(target, *criterion)
        else:
            return self

Model = TypeVar("Model", bound=BaseModel)
def _load_model(t: Type[Model], o: dict) -> dict:
    populated_keys = o.keys()
    required_keys = set(t.schema()['required'])
    missing_keys = required_keys.difference(populated_keys)
    if missing_keys:
        raise ValueError(f'Required keys missing: {missing_keys}')
    all_definition_keys = t.schema()['properties'].keys()
    return t(**{k: v for k, v in o.items() if k in all_definition_keys}).__dict__