
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
# import schema.Project
# from schema import User
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



router = APIRouter(prefix='/project_inside_path', tags=['project_inside_path'])








        
    # if path_new:
    #     check=os.chdir(path_new)
    #     check2=os.walk(check)
    #     inside=os.getcwd(check2)
    #     print("**********",inside)

    # for folderlist in dir_list:
    #     # last_path=path_new+'/'+folderlist
    #     print("++++++",folderlist)
#     print("pathlists",path_lists)
    # for new_path_list in dir_list:
    #     new_path=path_lists+"/"+new_path_list
    #     print("new_path",new_path)

    