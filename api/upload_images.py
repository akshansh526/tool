import os
import glob
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, status, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
import schema.Upload_images
import schema.Project
from database import SessionLocal, engine
import models
import mysql.connector
import database

# from api import folder_inside_folder
# import uvicorn
from passlib.context import CryptContext

# from pydantic import dict
import utils

# from api import upload_img_database
import aiofiles
from typing import List
import sys
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import sqlalchemy.exc
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text
import shutil
from api import make_folder

sys.path.append("..")


router = APIRouter(prefix="/upload_images", tags=["upload_images"])



import glob
'''@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}  '''


@router.post("/upload/{project_id}/{user_id}")
async def upload(
    project_id,
    user_id,
    files: List[UploadFile] = File(...),
    db: Session = Depends(database.get_db)
):     
    project_path1 = (
                db.query(models.Add_project.project_path)
                .filter(models.Add_project.project_id == project_id)
                .all()[-1]
                    )
    get_id=project_path1[0]
    print("gettttttttttttt",get_id) 
    for file in files:

        try:
            contents =   file.file.read()
            # print("conta",contents)
            path_img = get_id+"/"+ file.filename
            print(">>>>>>>path>>>>>>>>>>>",type(file.filename))
            with open(path_img, 'wb') as f:
                f.write(contents)
            save_path_img = models.Annotation_master()
            save_path_img.image_url = path_img
            save_path_img.project_id = project_id
            save_path_img.user_id = user_id
            print(">>>>", project_id)
            db.add(save_path_img)
            db.commit()
            print(">>>>>>>>>succesfully added", save_path_img)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
           await file.close()

    return {"message": f"Successfuly uploaded {[path_img for file in files]}"}  


@router.get("/all_images/projects/{project_id}/{user_id}")
async def get_all_images(
    project_id: int, user_id: int, db: Session = Depends(database.get_db)
):
    images = (
        db.query(models.Annotation_master)
        .filter(
            models.Annotation_master.project_id == project_id,
            models.Annotation_master.user_id == user_id,
        )
        .all()
    )
    print("aaaaaaaaaaaaaaaaaaaa", images)
    images_path=[]
    for image in images:
        images_path.append(image.image_url)
    print(images_path)
    response = {"project_id" : project_id ,"user_id" : user_id ,  "images_urls" : images_path}

    if images and image is None:
        return JSONResponse(status_code=404, content="No image found related to this project id")
    if images:
                return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"image with associated with this project id {project_id} is not found please upload images",)


#     return JSONResponse(status_code=201, content=response) 
# # {"message": f"images {[image for file in image]}"}  



@router.get("/all_images_count/projects/{project_id}/{user_id}")
async def get_all_images_count(
    project_id: int, user_id: int, db: Session = Depends(database.get_db)
):
    images = (
        db.query(models.Annotation_master)
        .filter(
            models.Annotation_master.project_id == project_id,
            models.Annotation_master.user_id == user_id,
        )
        .all()
    )
    images_count = db.query(models.Annotation_master.image_id).count()
    print("++++++++++++image_count++++++++++", images_count)
    print("++++++++++++image_count++++++++++", images)
    if images_count is None:
        return JSONResponse(
            status_code=404, content="No image  found related to this project id"
        )
    return JSONResponse(content=images,status_code=201)


@router.delete("/delete/{image_id}")
async def delete_images(image_id: int, db: Session = Depends(database.get_db)):
    filepath = (
        db.query(models.Annotation_master)
        .filter(models.Annotation_master.image_id == image_id)
        .first()
    )
    if filepath is None:
        return JSONResponse(status_code=404, content="No image found")
    try:
        os.remove(filepath[0])
    except FileNotFoundError:
        return JSONResponse(status_code=404, content="File not found in directory")
    delete = (
        db.query(models.Annotation_master)
        .filter(models.Annotation_master.image_id == image_id)
        .delete()
    )
    db.commit()
    # print(delete)
    if delete:
        return JSONResponse(status_code=200, content="Images deleted successfully")
    print(filepath[0])


@router.put("/image_path/{image_id}")
async def image_path(image_id: int, db: Session = Depends(database.get_db)):
    try:
        project_names = (
            db.query(models.Annotation_master.image_url)
            .filter(models.Annotation_master.image_id == image_id)
            .first()
        )
        new_path = "E:/Projects_folder" + project_names[0]
        print("*********************", new_path)

        db.query(models.Annotation_master).filter(
            models.Annotation_master.image_id == image_id
        ).update({"image_url": new_path})
        db.commit()
        return JSONResponse(status_code=201, content="image updated successfully")
    except sqlalchemy.exc.OperationalError:
        print("some error occured")
        return JSONResponse(status_code=400, content="some unexpected error occurred")

