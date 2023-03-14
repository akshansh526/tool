from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, status, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
from datetime import datetime, timedelta
from typing import Union
import schema.Project
import schema.User
from database import SessionLocal, engine
import models
import database
import sys

# from utils.utils import _load_model
import sqlalchemy.exc


import sys

sys.path.append("..")


router = APIRouter(prefix="/delete_project", tags=["delete_project"])


@router.delete("/delete/{project_id}/{user_id}")
async def delete_project(
    project_id: int, user_id: int, db: Session = Depends(database.get_db)
):
    try:

        user_map = (
            db.query(models.Delete_project_map)
            .filter(models.Delete_project_map.admin_id == user_id)
            .first()
        )
        db.commit()
        proj_map = (
            db.query(models.Delete_project_map)
            .filter(models.Delete_project_map.project_id == project_id)
            .first()
        )
        print(".......>>>>>", user_map)
        db.commit()
        proj_map = db.query(models.Add_project).all()
        print("+++++", proj_map)
        db.commit()

        delete = (
            db.query(models.Add_project)
            .filter(models.Add_project.project_id == project_id)
            .delete()
        )
        db.commit()

        if delete:
            return JSONResponse(status_code=200, content="Project deleted successfully")
        return JSONResponse(status_code=404, content="No project found")
    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting question with {project_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")
