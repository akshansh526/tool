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

    return {"image_path_lists": [path_img for file in files]}  


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
    try:
    
    
        filepath = (
            db.query(models.Annotation_master.image_url
            )
            .filter(models.Annotation_master.image_id == image_id)
            .first()
        )[0]
        print(">>>>>>",filepath)

        delete = (
        db.query(models.Annotation_master)
        .filter(models.Annotation_master.image_id == image_id)
        .delete()
            )
      
        os.remove(filepath
        )
    
        db.commit()
        if delete:
                return JSONResponse(status_code=200, content="Image deleted successfully")
        return JSONResponse(status_code=404, content="No image found")
    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting image with {image_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")


@router.put("/rename_image/{image_id}")
async def rename_image(image_id: int, rename:schema.Upload_images.Rename_image, db: Session = Depends(database.get_db)):
    
    image_path_query=db.query(models.Annotation_master.image_url).filter(models.Annotation_master.image_id==image_id).all()[0][0]
    print("++++++++++++++",image_path_query)
    spl=image_path_query.split("/")
    name=spl[-1]
    print("++++++++++++++",spl)
    print("+++++++name+++++++",name)
    s = "/"
    s = s.join(spl[0:-1])
    print(s)
    new_spl=spl
  
    img=[rename.image_name][0]
    print("************",img)
    new_spl[-1]=img
    print("************",new_spl)
    s2='/'
    s2=s2.join(new_spl)
    print("************",s2)
    data={"image_url":s2}
    
    image_path_query2=db.query(models.Annotation_master).filter(models.Annotation_master.image_id==image_id).update(data)
    db.commit()
    old_name = image_path_query
    new_name = s2

  
    
 
    try:
                os.replace(image_path_query, s2)
                print("Source path renamed to destination path successfully.")
    except IsADirectoryError:
                print("Source is a file but destination is a directory.")
    except NotADirectoryError:
                print("Source is a directory but destination is a file.")
    except PermissionError:
                print("Operation not permitted.")
    except OSError as error:
                print("not permitted.")
 
    
    if image_path_query:
                    return data
    else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"image with associated with this project id {image_id} is not found please upload images",)

   

