import shutil
import os
import pathlib
from pathlib2 import Path
import re
from datetime import datetime
import os
from fastapi import Depends, FastAPI, APIRouter, Request, status, Form
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import re
from starlette.exceptions import HTTPException
from datetime import datetime, timedelta
from typing import Union, List
import schema.Project
import schema.User
from database import SessionLocal, engine
import models
import database
import sys
from api import make_folder
import sqlalchemy.exc
from sqlalchemy import select

import os
from sqlalchemy import insert
import sys
from api import auth




today = datetime.now()



with Session(engine) as session:
    users=session.query(models.User_details).all()
    for user_list in users:
        print("users>>>>>>>",user_list.user_id)
        if user_list.user_id not in users:
            user_name=session.query(models.User_details.first_name).filter(models.User_details.user_id).all()[-1]
            get_id2=user_name[0]
            print("!!!!!!!!!!!!!!!!!!!",get_id2)
    print("users",users)
    

path="E:/Projects_folder"


def folder(a):

    path1 = path + "/" + a
    today = datetime.now()
    
    
    if not os.path.isdir(path1):
        os.mkdir(path1+today.strftime('%d%m%Y')+get_id2)
        print(">>>>>>>>>>folder_created>>>>>>>>")
       
    else:
        print("Already folder created")
    path2=os.path.join(path1+today.strftime('%d%m%Y'))
    print(">>>>path2>>>>>",path2)
    return path2


  


def folder2(a):
    path1 = path + "/" + a
    path2 = path1 + "/" + a + "1"
    print(">>>>>>>>>>>>>>", path1)
    if not os.path.isdir(path1):
        os.mkdir(path1)
        print("folder_created")
    else:

        print("Already folder created")
    if not os.path.isdir(path2):
        os.mkdir(path2)
        print("inside folder_created")
    else:

        print("Already folder created")
    print(path2)
    return path2
    

def create_folder(a):
    path1 = "E:/Projects_folder"
    i = 1
    while True:

        if not os.path.isdir(path1):
            os.mkdir(path1)
            # print(">>>>>>>",path1)
        if len(os.listdir(path1)) >= 100:
            path2 = path1 + str(i)
            print(">>>>>>", path2)
            if not os.path.isdir(path2):
                os.mkdir(path2)
                i += 1
                path1 = path2
                print(">>>>>>", path1)
