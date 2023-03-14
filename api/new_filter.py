import logging
from typing import Any, AsyncIterator, List, Optional

import uvicorn

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, event, select
from sqlalchemy.engine import Engine

from sqlalchemy.orm import Mapped, declarative_base, relationship

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from fastapi import Depends,APIRouter, Request
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
import sqlalchemy
import schema.User
from database import SessionLocal, engine
import models
import database
from schema import Assign
import sqlalchemy.exc
import sys
import random
from operator import length_hint
from typing import List ,Optional
from collections import deque




router = APIRouter(prefix="/filter_new", tags=["filter_new"])

class projectOut(BaseModel):
    project_id: int
    project_name: str
    project_path: str
    

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    first_name: str
    email: str
    phone_no: int
     

class UserOut(UserIn):
    id: int
    project_assigned: Optional[projectOut]

    class Config:
        orm_mode = True


# class AddressFilter(Filter):
#     street: Optional[str]
#     country: Optional[str]
#     city: Optional[str]
#     city__in: Optional[List[str]]
#     custom_order_by: Optional[List[str]]
#     custom_search: Optional[str]

#     class Constants(Filter.Constants):
#         model = Address
#         ordering_field_name = "custom_order_by"
#         search_field_name = "custom_search"
#         search_model_fields = ["street", "country", "city"]


class UserFilter(Filter):
    first_name: Optional[str]
    name__first_name: Optional[str]
    name__first_name: Optional[str]
    name__first_name: Optional[str]
    # address: Optional[AddressFilter] = FilterDepends(with_prefix("address", AddressFilter))
    # age__lt: Optional[int]
    # age__gte: int = Field(Query(description="this is a nice description"))
    # """Required field with a custom description.
    # See: https://github.com/tiangolo/fastapi/issues/4700 for why we need to wrap `Query` in `Field`.
    # """
    order_by: List[str] = ["first_name"]
    search: Optional[str]

    class Constants(Filter.Constants):
        model = models.User_details
        search_model_fields = ["first_name"]









@router.get("/users", response_model=List[UserOut])
async def get_users(
    user_filter: UserFilter = FilterDepends(UserFilter),
    db: Session = Depends(database.get_db),
) -> Any:
    query = select(models.User_details).join(models.Add_project)
    query = user_filter.filter(query)
    query = user_filter.sort(query)
    result = db.execute(query)
    return result.scalars().all()


# @app.get("/addresses", response_model=List[AddressOut])
# async def get_addresses(
#     address_filter: AddressFilter = FilterDepends(with_prefix("my_prefix", AddressFilter), by_alias=True),
#     db: AsyncSession = Depends(get_db),
# ) -> Any:
#     query = select(Address)
#     query = address_filter.filter(query)
#     query = address_filter.sort(query)
#     result = await db.execute(query)
#     return result.scalars().all()


# if __name__ == "__main__":
#     uvicorn.run("fastapi_filter_sqlalchemy:app", reload=True)