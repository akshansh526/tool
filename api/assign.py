from fastapi import Depends,APIRouter, Request,status
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
from itertools import tee
from schema import Qc
from itertools import groupby
from operator import itemgetter
from starlette.exceptions import HTTPException
 
sys.path.append("..")


router = APIRouter(prefix="/assign_to", tags=["assign_to"])


def image_count(a, b):

    return a / b







@router.post("/Assign_to/{project_id}")
async def Assignto(
    project_id:int, 
    assign_details: schema.Assign.Assign_to,
    user_name:schema.User.User_map, 
    db: Session = Depends(database.get_db)
):      
# dictionary
        
        

        # def split_on_condition(seq, condition):
        #     l1, l2 = tee((condition(item), item) for item in seq)
        #     return (i for p, i in l1 if p), (i for p, i in l2 if not p)
        
        assign_models=models.Assign_to()
                
        user_lists=assign_details.user_id
        image_lists=assign_details.image_id 
        assigned_by_list=assign_details.assigned_by
        # print("image_lists",image_lists)  
        # print("user_lists",user_lists)
        # print("assigned_by_list",assigned_by_list)
        user_len=len(user_lists)
        # print("user_len",user_len)
        image_len=len(image_lists)
        # print("image_len",image_len)
        div=int(image_len/user_len)
        # print("division",div)
        a=div
        user_dict={}
        j=0           
        for k,i in enumerate(user_lists):
            print(">>>>>>>",k)
            print(">>>>>>>",i)
            if k<(user_len-1):  
                list=[]
                print("############",i,k)
                print(type(i))
                while j<div:

                    print("JJJJJJJJJJJJJJJJJJJ",j)
                    try:
                        list.append(image_lists[j])
                        
                    except:
                        print()
                    j+=1
                j=j
                
                    
                user_dict[i]=list
                list=[]
                div=div+a 
                print("^^^^^^^^^^^^^^^^^^",div)
                print("$$$$$$$$$$$$$",j)
            elif k==(user_len-1):
                 list=image_lists[j:image_len]
                 user_dict[i]=list
                 print("!!!!",user_dict)
                 print("+++++",list[0:3])
                 


        
        values_to_insert=[]
        for key in user_dict.keys():
             print("@@@@@@",key)
             for img in user_dict[key]:
                    print("*****",img)
                    values_to_insert.append(models.Assign_to(image_id=img,user_id=key,project_id=project_id,assigned_by=assign_details.assigned_by))

    
       

        db.add_all(values_to_insert)
        db.commit()
        users = db.query(models.User_details).filter_if(user_name.first_name is not None, models.User_details.first_name == user_name.first_name).all()
        # print("+++++++",users)
        print("user_dict",user_dict)
        return JSONResponse(content=user_dict)
        # return user_dict,user_name



@router.get("/assign_details_by_user/{user_id}")
async def get_all_assign_details(user_id:int,db: Session = Depends(database.get_db)):

    assigned = db.query(models.Assign_to).filter(models.Assign_to.user_id==user_id).all()
    assigned_image_count=db.query(models.Assign_to.image_id).filter(models.Assign_to.user_id==user_id).count()
    for assign in assigned:
                 print(assign.assign_id)
    if assigned:
            return {
                "assigned":assigned
                    }
    else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"no details found  with this user id {user_id} is not available",)


@router.post("/reviewer_mapping/{user_id}")
async def reviewer_mapping(
    
    user_id:int, 
    assign_details: schema.Assign.Reviewer,
    db: Session = Depends(database.get_db)
):      

        
        assign_models=models.Map_reviewer()
        users_list=assign_details.annotator_user_id

        print("****************",users_list)

        
        values_to_insert=[]
        for key in users_list:
                print("@@@@@@",key)
                values_to_insert.append(
                       models.Map_reviewer(annotator_user_id=key,reviewer_id=assign_details.reviewer_id)
                                       )
        db.add_all(values_to_insert)
        db.commit()       
        return {"reveiwers":values_to_insert}
        


@router.get("/get_details_by_reviewer/{reviewer_id}")
async def get_details_by_reviewer(reviewer_id:Optional[int],db: Session = Depends(database.get_db)):

    reviewers = db.query(models.Map_reviewer).filter(models.Map_reviewer.reviewer_id==reviewer_id).all()
    
    for re in reviewers:
                print(re.reviewer_id)
    if reviewers:
                return {
                    "reviewers":reviewers
                       }
    else:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f" {user_id} is not found",)
    




@router.get("/get_annotations_by_user/{user_id}")
async def annot_by_user(user_id: int, db: Session = Depends(database.get_db)):
    image_list = (
        db.query(models.Assign_to)
        .filter(models.Assign_to.user_id == user_id)
        .all()
    )
    print("################",image_list)
    if image_list:
                   return {
                    "images_list":[images.image_id for images in image_list]
                           }
    else:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no images assigned with this {user_id} user_id ")
