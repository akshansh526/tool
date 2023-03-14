from fastapi import Depends, APIRouter, Request
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import schema.User
import models
import database
from schema import User

# import uvicorn
from api import make_folder
from passlib.context import CryptContext

import sqlalchemy.exc
import sys
sys.path.append("..")
import os
import fileinput


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return bcrypt_context.hash(password)


# def get_password_hash_2(confirm_password):
#     return bcrypt_context.hash(confirm_password)


def verify_password(hashed_password, plain_password):
    return bcrypt_context.verify(plain_password, hashed_password)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    request: Request,
    user_details: schema.User.UserCreate,
    db: Session = Depends(database.get_db),
):
    user_model = models.User_details()
    print("user_model", user_model)
    user_model.first_name = user_details.first_name
    user_model.last_name = user_details.last_name
    user_model.email = user_details.email
    user_model.password = get_password_hash(user_details.password)
    user_model.phone_no = user_details.phone_no
    user_model.roles_id = 1
    user_model.organisation_name = user_details.organisation_name

    db.add(user_model)
    db.commit() 

  
    if user_model:
        return JSONResponse(status_code=200, content="user created successfully")
    
    
    return JSONResponse(content={"detail": "User Create Successfully"}, status_code=200)


@router.post("/login", response_model=schema.User.UserOut)
async def login(
    user_details: schema.User.UserOut, db: Session = Depends(database.get_db)
):
    print("@@222", user_details.__dict__)
    email_validation_query = (
        db.query(models.User_details)
        .filter(models.User_details.email == user_details.email)
        .first()
    )
    user_validation_query = (
        db.query(models.User_details).filter(models.User_details.roles_id == 2).first()
    )
    if email_validation_query:
        print(email_validation_query.__dict__["password"])
        if verify_password(
            email_validation_query.__dict__["password"], user_details.password
        ):
            # print(password_validation_query.__dict__)
            user = (
                db.query(models.User_details)
                .filter(models.User_details.email == user_details.email)
                .first()
            )
            return user
        if user_validation_query.is_admin:
            # print(password_validation_query.__dict__)
            user_val = (
                db.query(models.User_details)
                .filter(models.User_details.roles_id == 2)
                .first()
            )
            return user_val
        #  return user_model
        return JSONResponse(content={"detail": "you are not a  admin"}, status_code=401)

    # print(email_validation_query.__dict__)
    return JSONResponse(status_code=404, content="no user found")




@router.get("/all_admins")
async def get_all_admins(db: Session = Depends(database.get_db)):
    # projects = db.query(models.Add_project).all()
    admins = (
        db.query(models.User_details).filter(models.User_details.roles_id == 1).all()
    )
    for admin in admins:
        print(admin.first_name)
    print(">>>>>>>>>>>>>>>>>>", admin)
    if admins is None:
        return JSONResponse(status_code=404, content="No admins found with this name")
    return admins


@router.post("/user_create/{user_id}")
async def register_user(
    user_id: int,
    user_details: schema.User.UserCreate,
    db: Session = Depends(database.get_db),
):
    user_model = models.User_details()
    print("user_model", user_model)
    user_model.first_name = user_details.first_name
    user_model.last_name = user_details.last_name
    user_model.email = user_details.email
    user_model.password = get_password_hash(user_details.password)
    user_model.phone_no = user_details.phone_no
    user_model.roles_id = 2
    user_model.organisation_name = user_details.organisation_name

    db.add(user_model)

    db.commit()

    mapped_user = (
        db.query(models.Map_user).filter(models.Map_user.user_id == user_id).first()
    )
    mapped_user2 = (
        db.query(models.User_details.user_id)
        .where(models.User_details.roles_id == 2)
        .all()[-1]
    )
    mapped_user3 = mapped_user2[0]
    print(">>>>>>>>>>", mapped_user2)
    print(">>>>>>>>>>", mapped_user3)

    user_map_model = models.Map_user()
    user_map_model.admin_id = user_id
    user_map_model.user_id = mapped_user3
    print("+++++++", user_map_model)
    db.add(user_map_model)
    db.commit()

    return JSONResponse(
        content={"detail": "User created Successfully"}, status_code=200
    )


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    try:
        fetch = (
            db.query(models.User_details)
            .filter(models.User_details.user_id == user_id)
            .all()
        )

        delete = (
            db.query(models.User_details)
            .filter(models.User_details.user_id == user_id)
            .delete()
        )
        db.commit()

        if delete:
            return JSONResponse(status_code=200, content="user deleted successfully")
        return JSONResponse(status_code=404, content="No user found")
    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting user with {user_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")


@router.get(
    "/all_users_by_admin/{admin_id}",
)
async def get_all_users_by_admin(admin_id: int, db: Session = Depends(database.get_db)):
    # projects = db.query(models.Add_project).all()
    users = (
        db.query(models.Map_user).filter(models.Map_user.admin_id==admin_id).all()
    )
    print("?????????", users)

    if users is None:
        return JSONResponse(status_code=404, content="No users found with this name")

    return users

@router.get("/map_user/{user_id}")
async def map_users(user_id:int,db:Session=Depends(database.get_db)):
    mapping=db.query(models.Map_user).filter(models.Map_user.user_id==user_id).all()

    print("mapping",mapping)

    if mapping is None:
        return JSONResponse(status_code=404, content="No users found with this name")
    return mapping