#Twitter: Bek Brace
#Instagram: Bek Brace

import uvicorn
from fastapi import FastAPI, Body, Depends

from api.scheme import UserSchema,UserLoginSchema
from auth_bearer import JWTBearer
from auth_handler import signJWT
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



users = []

app = FastAPI()



def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers

# testing
@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!."}


# Get Posts
# @app.get("/posts", tags=["posts"])
# def get_posts():
#     return { "data": posts }


# @app.get("/posts/{id}", tags=["posts"])
# def get_single_post(id: int):
#     if id > len(posts):
#         return {
#             "error": "No such post with the supplied ID."
#         }

#     for post in posts:
#         if post["id"] == id:
#             return {
#                 "data": post
#             }


# @app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# def add_post(post: PostSchema):
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return bcrypt_context.hash(password)


# def get_password_hash_2(confirm_password):
#     return bcrypt_context.hash(confirm_password)


def verify_password(hashed_password, plain_password):
    return bcrypt_context.verify(plain_password, hashed_password)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/user/signup")
def create_user(user: UserSchema = Body(...),db: Session = Depends(database.get_db)):
    user_model = models.User_details()
    print("user_model", user_model)
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.email = user.email
    user_model.password = user.password
    user_model.phone_no = user.phone_no
    user_model.roles_id = 1
    user_model.organisation_name = user.organisation_name

    db.add(user_model)
    db.commit() 

  
    # if user_model:
    #     return JSONResponse(status_code=200, content="user deleted successfully")
    
    
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
