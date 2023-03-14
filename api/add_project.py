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


router = APIRouter(prefix="/add_project", tags=["add_project"])


@router.post("/Add_project/{user_id}}")
async def Create_projects(
   
    user_id: int,
    add_project: schema.Project.Project_create,

    db: Session = Depends(database.get_db),
):
    try:
        user_name=db.query(models.User_details.first_name).filter(models.User_details.user_id).all()[-1]
        db.commit()
        add_project_model = models.Add_project()
        add_project_model.user_id = user_id
        add_project_model.project_name = add_project.project_name
        add_project_model.description = add_project.description
        add_project_model.industries_name = add_project.industries_name
        add_project_model.start_date = add_project.start_date
        add_project_model.enddate = add_project.enddate
        add_project_model.approved_by=add_project.approved_by
        abc = add_project.project_name
        print("schema>>>>>>>>>>>>>",add_project)
        print("schema>>>>>>>>>>>>>",add_project.project_name)

        
        fold = make_folder.folder(abc)
        db.add(add_project_model)
        db.commit()
        
        print("****user_name******",user_name)
        p_id = (
            db.query(models.Add_project.project_id)
            .filter(models.Add_project.project_id)
            .all()[-1]
        )
        
        get_id = p_id[0]
        get_id2=user_name[0]
        print("#######get_id#####",get_id2)
        pro_path = (
            db.query(models.Add_project)
            .filter(models.Add_project.project_id == get_id)
            .update({"project_path": fold+get_id2})
        )
        db.commit()
        # print("*********", pro_path)
        print("")



        class_models=models.Add_classes()
                
        class_lists=add_project.class_name

        print("clasessssssssssss",class_lists) 
        values_to_insert=[]
        for key in class_lists:
           print("key",key)
           values_to_insert.append(models.Add_classes(class_name=key,user_id=user_id,project_id=get_id))
        
       
        db.add_all(values_to_insert)
        db.commit()


        return JSONResponse(status_code=201, content="Project created successfully")
    except sqlalchemy.exc.OperationalError:
        print("some error occured")
        return JSONResponse(status_code=400, content="some unexpected error occurred")

    
#
@router.get("/all_project")
async def get_all_project(db: Session = Depends(database.get_db)):
    # projects = db.query(models.Add_project).all()
    projects = db.query(models.Add_project).all()
    for project in projects:
        print(project.project_name)
    print(">>>>>>>>>>>>>>>>>>", project)
    if projects is None:
        return JSONResponse(status_code=404, content="No project found with this id")
    return projects
@router.put("/update_classes_name/{project_id}/{class_id}")
async def update_classes_name(project_id:int,class_id:int,class_schema:schema.Project.Update_name,db:Session=Depends(database.get_db)):
     
     update_class_name=models.Add_classes() 
     update_class_name.class_name=class_schema.class_name
     

     update_classes=db.query(models.Add_classes).filter(models.Add_classes.class_id==class_id).update({"class_name":class_schema.class_name})

     db.commit()

     return  JSONResponse(status_code=201, content="updated successfully")



@router.get("/get_project_by_admin/{user_id}")
async def get_project_by_admin(user_id: int, db: Session = Depends(database.get_db)):

            projects = (
                db.query(models.Add_project).filter(models.Add_project.user_id == user_id).all()
            )
    # projects=db.query(models.Add_project).all()
            for project in projects:
                print(project.project_name)
    
            if projects:
                return {"projects":projects[0:-1]}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Project with associated with this user id {user_id} is not available",)
   


@router.get("/get_folder_path_by_project_id/{project_id}")
async def get_folder_path_by_project_id(
    project_id: int, db: Session = Depends(database.get_db)
):

    projects = (
        db.query(models.Add_project)
        .filter(models.Add_project.project_id == project_id)
        .all()
    )
    print("++++++++++++", projects)
    for project in projects:
        print(project.project_path)
    path = project.project_path
    print("^^^^^^^^^", path)
    if projects is None:
        return JSONResponse(status_code=404, content="No project found with this id")
    return projects and path

@router.put('/project_edit/{project_id}')
async def project_edit(project_id:int,edit:schema.Project.Edit_project,db:Session=Depends(database.get_db)):
   
   
    data={"project_name":edit.project_name,"project_path":edit.project_path,"approved_by":edit.approved_by,"industries_name":edit.industries_name,"description":edit.description}
    update_project_name=db.query(models.Add_project).filter(models.Add_project.project_id==project_id).update(data)
   

    db.commit()

    return  JSONResponse(status_code=201, content="updated successfully")



# @router.post('/project_edit')
# async def project_edit(appr:schema.Project.Project_get,db:Session=Depends(database.get_db)):
 
#     project=db.query(models.Add_project).filter(models.Add_project.is_active==False).all()
#     project2=db.query(models.Add_project).filter(models.Add_project.is_active==True).all()
#     project_3=db.query(models.Add_project).filter_by()
#     projects=db.query(models.Add_project).filter(models.Add_project.enddate).all()
#     for pro in projects:
#         print(pro.project_name)
    
#     print("project_3",project_3)

#     print("project",project)
#     print("project",projects)
    
    
    
    # print("***********",edit_query)

    # db.commit()
    
    # return project,project2




@router.post('/project_inside_path/{project_id}')
async def project_inside_path(project_id:int, db: Session = Depends(database.get_db)):
            projects_path_new=db.query(models.Add_project.project_path).filter(models.Add_project.project_id==project_id).all()
            projects_path=db.query(models.Add_project.project_path).filter(models.Add_project.project_id).all()
            print("projects ids",)
            inside_model=models.Project_inside_folder_map()
            inside_model.related_project_id=project_id
            
            
            pro_path="E:/Projects_folder"
            dir_list=os.listdir(pro_path)
            print("dir_list",dir_list)
            
            
            path_dict={}
            j=0           
            
            



            tl = projects_path
            path_list=[item[0] for item in tl]
            for k in path_list:
                print(">>>>>>>",k)
              
                
                list=[]
                print("############",k)
                # print(type(i))
                
                k=k

                    
                        
                path_dict[k]=list
                list=[]
            # [tl[0] for tl in ]
            print("?????????????????",path_list)
            for path_new in path_list:
                           print("&&&&&&&&&&&&&&",str(path_new))

                           many=[x[0] for x in os.walk(str(path_new))]
                           print("mmmmmmmmmmmmmmmmmmmmmmmmm",many)
                           for latest_path in many:
                                print("latestpath",latest_path)
                                path_dict={}
                                values_to_insert=[]
                                for key in path_dict.keys():
                                    print("^^keys^^^",key)
                                    values_to_insert.append(models.Project_inside_folder_map).filter_by(project_id=key,folder_path=latest_path)
                                    continue
                                    for paths in path_dict[key]:
                                        print("++++++",paths)
                                print("vvvvvvvvvvvvvvvvvvvvv",values_to_insert)
            
            # print("!!!!!!!!!!!!!!!!!!!",type(get_id2))


        

            db.add_all(values_to_insert)
            db.commit()
                        
            return JSONResponse(content=latest_path,status_code=201)




@router.get('/project_status/{user_id}')
async def project_status(user_id:int,db:Session =Depends(database.get_db)):
    project_count=db.query(models.Add_project).filter_by(is_active = 1).count()
    project_count1=db.query(models.Add_project).filter_by(is_active = 1).all()[0:-1]
    for projects in project_count1:
        print(":::::::::",projects.project_name)
    approved_count1=db.query(models.Add_project).filter_by(approved_status = 1).count()

    approved_count2=db.query(models.Add_project).filter_by(approved_status=1).all()
    for app in approved_count2:
        print(":::::::::::::::",app.project_name)
    
    print("******>>>>>>>>>>**********",approved_count1)
    
    print("****************",project_count1)
    if projects:
            return {
                "active_projects":[projects for projects in project_count1],
                "approved_projects":[app for app in approved_count2],
                "Count_of active projects":project_count,
                "total_no_of_approved_projects":approved_count1
                   }
    else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with associated with this user id {user_id} is not available",)
    # return  [projects for projects in project_count1]