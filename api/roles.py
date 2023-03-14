from fastapi import Depends,  APIRouter, Request,status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
from datetime import datetime, timedelta
from typing import Union
from database import SessionLocal, engine
import models
import database
import schema.Roles
from sqlalchemy import insert
from starlette.exceptions import HTTPException
# from pydantic import dict
import sqlalchemy.exc
import sys

sys.path.append("..")


router = APIRouter(prefix="/Create_roles", tags=["Create_roles"])


@router.post("/create_roles")
async def create_roles(
    request: Request,
    roles_details: schema.Roles.Create_roles,
    db: Session = Depends(database.get_db),
):

    roles_model = models.Roles()
    roles_model.roles_name = roles_details.roles_name
    roles_model.roles_description = roles_details.roles_description
    db.add(roles_model)
    db.commit()
    return JSONResponse(
        content={"detail": "Roles Created Successfully"}, status_code=200
    )


@router.get("/get_all_roles")
async def get_all_roles(db: Session = Depends(database.get_db)):
    roles = db.query(models.Roles).all()
    for role in roles:
        print(">>>>>>>>", role.roles_name)
    print(">>>>>>>>>>>>>>>>>>", role)
    if roles:
            return {"roles":roles[0:-1]}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no details found  with this user id is not available",)


@router.delete("/delete_roles/{roles_id}")
async def delete_roles(roles_id: int, db: Session = Depends(database.get_db)):

    try:
        delete_role = (
            db.query(models.Roles).filter(models.Roles.roles_id == roles_id).delete()
        )

        if delete_role:
            return JSONResponse(status_code=200, content="roles deleted successfully")
        return JSONResponse(status_code=404, content="No roles found")

    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting question with {roles_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")

