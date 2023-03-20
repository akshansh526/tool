from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, status, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
from datetime import datetime, timedelta
from typing import Union
import schema.Project
import schema.User
import schema.Annotation
import schema.Shapebox
from database import SessionLocal, engine
import models
import database
import sys
from api import make_folder
# from utils.utils import _load_model
import sqlalchemy.exc
from sqlalchemy import select
# import uvicorn
import os
# from pydantic import dict

import sys

sys.path.append("..")





router = APIRouter(prefix='/shapebox', tags=['shapebox'])


@router.post('/shapebox')
async def shapebox(request: Request, shapebox_map: schema.Shapebox.ShapeBoxIn, db: Session = Depends(database.get_db)):
    try:   
        shapebox_model = models.Shapebox()
        shapebox_model=shapebox_map.shapebox_name
       
        db.add(shapebox_model)
        db.commit()
    
        return JSONResponse(status_code=201, content=' shapebox created successfully')
    except sqlalchemy.exc.OperationalError:
        print('some error occured')
        return JSONResponse(status_code=400, content='some unexpected error occurred')



@router.get('/all_shapeboxes')
async def get_all_shapeboxes( db: Session = Depends(database.get_db)):
    # projects = db.query(models.Add_project).all()
    annotations=db.query(models.Shapebox).all()
    for annotation in annotations:
        print(annotation.shapebox_name)
    print(">>>>>>>>>>>>>>>>>>" ,annotation)
    if annotations is None:
        return JSONResponse(status_code=404, content='No anonotations found with this id')
    return annotations




@router.delete('/delete/{shapebox_id}')
async def delete_shapeboxes(shapebox_id: int, db: Session = Depends(database.get_db)):
    try:
        delete = db.query(models.Shapebox).filter(models.Shapebox.shapebox_id == shapebox_id).delete()
        db.commit()
        if delete:
            return JSONResponse(status_code=200, content='Shapeboxes deleted successfully')
        return JSONResponse(status_code=404, content='No Shapebox found')
    except sqlalchemy.exc.OperationalError:
        print(f'error occurred while deleting annotations with {shapebox_id} id')
        return JSONResponse(status_code=503, content='unexpected error occurred')

