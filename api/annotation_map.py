from fastapi import Depends, APIRouter,status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import schema.Project
import schema.User
import schema.Annotation
import models
import database
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, JSON
import sys
import json
import sqlalchemy.exc
import sys
from typing import Optional,List,Dict,Union
from sqlalchemy import update, func, bindparam
from starlette.exceptions import HTTPException
from flask import jsonify
sys.path.append("..")
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


router = APIRouter(prefix="/map_annotation", tags=["map_annotation"])


def func1(data):
    for key, value in data.items():
        print(str(key) + "->" + str(value))

        if type(value) == type(dict()):
            func1(value)
        elif type(value) == type(dict()):
            for val in value:
                if type(val) == type(str()):
                    pass
                elif type(val) == type(dict()):
                    pass
                else:
                    func1(val)
    print("????????", key, value)

class CoordBase(BaseModel):
        class_coord: List[Dict[str, List[float]]]

class CoordCreate(CoordBase):
        pass

class Coord(CoordBase):
    id: int

    class Config:
        orm_mode = True



@router.post("/Annotation_map/{project_id}/{user_id}/{image_id}/{class_id}")
async def Mapping_annotations(
    user_id: int,
    Project_id: int,
    image_id: int,
    class_id:int,
    annotation_map: List[schema.Annotation.Object],
    db: Session = Depends(database.get_db),
):
    try:
       
        annotation_model_map= [ models.Image_annotation_mapping(project_id= Project_id, 
                user_id= user_id, image_id= image_id, class_id=class_id, bounding_boxes= i.coord ) for i in annotation_map]
        for annot in annotation_model_map:
            boxes=annot.bounding_boxes
            print (boxes)
            # print("mmmmmmmmmmmmmmmmmmmmmm",myDict)
                
            # for 
        
        
        db.add_all(annotation_model_map)
        db.commit()
        

        return JSONResponse(status_code=201, content=" annotation stored successfully")
    except sqlalchemy.exc.OperationalError:
        print("some error occured")
        return JSONResponse(status_code=400, content="some unexpected error occurred")


@router.get("/{class_id}")
async def get_cords_by_class(class_id: int, db: Session = Depends(database.get_db)):
    annotations =db.query(models.Image_annotation_mapping).filter(models.Image_annotation_mapping.class_id == class_id).all()
 

    for annotation in annotations:
        # print(annotation.bounding_boxes)
        points_dict={class_id:annotation.bounding_boxes}
        print("++++++",points_dict)
       
    # print([x.__dict__ for x in annotations])
    if annotations:
        return {"annotations":annotations}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with associated with this user id {image_id} is not available",)
  



@router.delete("/delete/{class_id}")
async def delete_annotations(class_id: int, db: Session = Depends(database.get_db)):
    try:
        delete = (
            db.query(models.Image_annotation_mapping)
            .filter(models.Image_annotation_mapping.class_id == class_id)
            .delete()
        )
        db.commit()
        if delete:
            return JSONResponse(
                status_code=200, content="Annotations deleted successfully"
            )
        return JSONResponse(status_code=404, content="No annotation found")
    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting annotations with {user_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")


@router.put('/update_annot/{class_id}')
async def update_annot(class_id:int, annotation_map: List[schema.Annotation.Object],db: Session = Depends(database.get_db)):
   


    

    update_boxes=[ db.query(models.Image_annotation_mapping).filter
                             (models.Image_annotation_mapping.class_id==class_id).
                                  update({"bounding_boxes":i.coord}) for i in annotation_map]
          
    db.commit()

    update_boxes2= db.query(models.Image_annotation_mapping.bounding_boxes).\
                              filter(models.Image_annotation_mapping.class_id==class_id).all()   
    db.commit()
    
    if update_boxes:
        return {"new_cords": update_boxes2 }
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f" cannot upadate  {class_id} is not available",)
  

            




@router.post('/qc_rejected_images/{image_id}/{user_id}/{project_id}')
async def qc_rejected_images(image_id:int,user_id:int,project_id:int, db:Session= Depends (database.get_db)):
      qc_model = models.Qc_image_map()
      qc_user_model=models.User_details()
      user_filter=db.query(models.User_details).filter_by(roles_id=1)
      print("user_filter>>>>>>>>>.",user_filter)
      qc_model.image_id=image_id
      qc_model.user_id=user_id
      qc_model.project_id=project_id
      db.add(qc_model)
      
      db.commit() 

      if qc_model:
                 return JSONResponse(status_code=201, content='rejected images sent successfully')
                 
      else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"image with associated with this project id {image_id,user_id,project_id} is not found please upload images",)
      


      
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]
# [121.12, 79.123, 456.123, 44.11]     

