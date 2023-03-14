import logging
from typing import Any, AsyncIterator, List, Optional
from models import Annotation_master,User_details
import uvicorn
from faker import Faker
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter 

# logger = logging.getLogger("uvicorn")


# @event.listens_for(Engine, "connect")
# def _set_sqlite_case_sensitive_pragma(dbapi_con, connection_record):
#     cursor = dbapi_con.cursor()
#     cursor.execute("PRAGMA case_sensitive_like=ON;")
#     cursor.close()


# engine = create_async_engine("sqlite+aiosqlite:///fastapi_filter.sqlite")

# async_session = sessionmaker(engine, class_=AsyncSession)

# Base = declarative_base()


# class Address(Base):
#     __tablename__ = "addresses"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     street = Column(String, nullable=False)
#     city = Column(String, nullable=False)
#     country = Column(String, nullable=False)


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     age = Column(Integer, nullable=False)
#     address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
#     address: Address = relationship(Address, backref="users", lazy="joined")


class ProjectsOut(BaseModel):
    project_id: int
    project_name: str

    class Config:
        orm_mode = True


class ImagesOut(BaseModel):
    image_id: int
    user_id:int
    project_id:int
    image_url: str

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    first_name: str
    last_name:str
    email: str
    


class UserOut(UserIn):
    user_id: int
    project_id: Optional[ProjectsOut]
    image_id:Optional[ImagesOut]

    class Config:
        orm_mode = True


class ImageFilter(Filter):
    user_id:Optional[int]
    project_id:Optional[int]
    image_id: Optional[List[int]]
    custom_order_by: Optional[List[str]]
    custom_search: Optional[str]

    class Constants(Filter.Constants):
        model = Annotation_master
        ordering_field_name = "custom_order_by"
        search_field_name = "custom_search"
        search_model_fields = ["user_id", "project_id", "image_id","image_url"]

    class Config:
        orm_mode = True 

class UserFilter(Filter):
    name: Optional[str]
    name__ilike: Optional[str]
    name__like: Optional[str]
    name__neq: Optional[str]
    address: Optional[ImageFilter] = FilterDepends(with_prefix("images", ImageFilter))
  
    order_by: List[str] = ["name"]
    search: Optional[str]

    class Constants(Filter.Constants):
        model = User_details
        search_model_fields = ["name"]

