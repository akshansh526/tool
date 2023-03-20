# from sqlalchemy.orm import Mapped, declarative_base, relationship
# from fastapi_filter import FilterDepends, with_prefix
# from fastapi_filter.contrib.sqlalchemy import Filter
# from typing import Any, AsyncIterator, List, Optional
# import click
# import uvicorn
# from faker import Faker
# from fastapi import Depends, FastAPI, Query,APIRouter
# from pydantic import BaseModel, Field
# from sqlalchemy import Column, ForeignKey, Integer, String, event, select
# from sqlalchemy.engine import Engine


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import sys
# # from utils.utils import CustomQuery
# from sqlalchemy import select,insert
# from utils import CustomQuery



# from fastapi import Depends, APIRouter,status
# from starlette.responses import JSONResponse
# from sqlalchemy.orm import Session
# import schema.Project
# import schema.User
# import schema.Annotation
# import models
# import database
# import sys
# import sqlalchemy.exc
# import sys
# from sqlalchemy import update, func, bindparam
# from starlette.exceptions import HTTPException

# router = APIRouter(prefix='/filters', tags=['filters'])



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



# class ProjectsOut(BaseModel):
#     project_id:int
#     project_name:str

    
#     class Config:
#         orm_mode = True


# class ImageOut(ProjectsOut):
#     image_id:int
#     projects:Optional[ProjectsOut]

#     class Config:
#         orm_mode = True

# class ImagesFilter(Filter):
#     image_url: Optional[str]
#     custom_order_by: Optional[List[str]]
#     custom_search: Optional[str]

#     class Constants(Filter.Constants):
#         model = models.Annotation_master()
#         ordering_field_name = "custom_order_by"
#         search_field_name = "custom_search"
#         search_model_fields = ["image_url"]


# class ProjectFilter(Filter):
#     project_name: Optional[str]
#     project_name__ilike: Optional[str]
#     project_name__like: Optional[str]
#     project_name__neq: Optional[str]
#     image_url: Optional[ImagesFilter] = FilterDepends(with_prefix("images", ImagesFilter))
#     age__lt: Optional[int]
#     order_by: List[str] = ["image_url"]
#     search: Optional[str]

#     class Constants(Filter.Constants):
#         model = models.Add_project()
#         search_model_fields = ["project_name"]



