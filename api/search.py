
from fastapi import Depends, FastAPI, APIRouter, Request, status, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
from starlette.exceptions import HTTPException
from datetime import datetime, timedelta
from typing import Union, List
import schema.Project
import schema.User
import schema.Classes
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
from sqlalchemy import insert
import sys
from api import auth

sys.path.append("..")


router = APIRouter(prefix="/search", tags=["search"])








@router.get('/', response_model=Union[
    List[schema.Project.Project_get], List[schema.User.User_get]])
async def search(query: str,  db: Session = Depends(database.get_db)):
    match (type):
        case 'projects':
            records = db.query(models.Add_project).filter((models.Add_project.project_name.contains(query))).all()
                            
            return records        
        # case 'video':
        #     records = db.query(models.VideoMaster).filter(
        #         (models.VideoMaster.title.contains(query))# | (models.VideoMaster.url.contains(query)))            ).all()
        #     response = []
        #     if not records:
        #             records= db.query(models.VideoMaster).all()
        #     for i in records:
        #             response.append({
        #                 "video_id": i.video_id,
        #                 "url": i.url,
        #                 "title": i.title,
        #                 "assessment_id": i.assessment[0].__dict__['assessment_id']
        #             })
        #         # print(_load_model(schema.assessment.AssessmentAndVideoMapping, i.__dict__))                # print(i.assessment[0].__dict__['assessment_id'])            if response is None:
        #         return JSONResponse(status_code=404, content='No videos found')
        #     # print(response)            return response        case 'assessment':
        #     records = db.query(models.Assessments).filter(
        #         (models.Assessments.title.contains(query) | (models.Assessments.description.contains(query)))
        #     ).all()
        #     # print(records)            return records        case 'question':
            records = []
            question_ids = db.query(models.Add_project.project_id).filter((models.Add_project.project_name.contains(query))).all()
            for (project,) in question_ids:
                records.append(await get_question_by_id(project, db=db))
            return records