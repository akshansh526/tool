from fastapi import Depends, FastAPI, APIRouter, Request, status, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
from datetime import datetime, timedelta
from typing import Union
import schema.Project
import schema.User
import schema.Classes
from database import SessionLocal, engine
import models
import database
import sys
from starlette.exceptions import HTTPException
# from utils.utils import _load_model
import sqlalchemy.exc

# import uvicorn

router = APIRouter(prefix="/add_classes", tags=["add_classes"])


@router.post("/Add_classes/{project_id}")
async def AddClasses(
    project_id:int,
    user_id:int,
    add_class: schema.Classes.Add_classes,
    db: Session = Depends(database.get_db),
):
       
        add_class_model = models.Add_classes()
        add_class_model.user_id=user_id
        add_class_model.project_id=project_id
        add_class_model.class_name = add_class.class_name
        db.add(add_class_model)
        db.commit()

        return JSONResponse(status_code=201, content="classes created successfully")
  
     


@router.get("/all_classes/{project_id}")
async def get_all_classes_by_project_id(project_id:int,db: Session = Depends(database.get_db)):
    
    classes = db.query(models.Add_classes.class_name).filter(models.Add_classes.project_id==project_id).all()
    for classes_name in classes:
        print(classes_name.class_name)
    print(">>>>>>>>>>>>>>>>>>", classes)
    
    if classes:
            return {"classes_list":classes[0:-1]}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no details found  with this user id {project_id} is not available",)



@router.delete("/delete/{class_id}")
async def delete_class(class_id: int, db: Session = Depends(database.get_db)):
    try:
        delete = (
            db.query(models.Add_classes)
            .filter(models.Add_classes.class_id == class_id)
            .delete()
        )
        db.commit()
        if delete:
            return JSONResponse(status_code=200, content="classes deleted successfully")
        return JSONResponse(status_code=404, content="No class found")
    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting question with {class_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")
