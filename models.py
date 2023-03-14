from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, BigInteger,Float,JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import types
from sqlalchemy.dialects.mysql.base import MSBinary
from sqlalchemy.schema import Column
from sqlalchemy.schema import Column
from database import engine, Base
import datetime
import sys
import uuid
sys.path.append("..")


Base.metadata.create_all(engine)

class Annotation_master(Base):
     __tablename__='annotation_master'
     
     image_id=Column(Integer, primary_key=True, index=True)
     image_url=Column(String(255))
     project_id=Column(Integer,ForeignKey('add_project.project_id'))
     user_id=Column(Integer, ForeignKey('user_details.user_id'))
     dateCreated=Column(DateTime,default=func.now())
     
     
     image_user=relationship("User_details",back_populates='Annotation_master')
     master_image=relationship("Image_annotation_mapping")
     assign_image=relationship("Assign_to")
    #  image_rel=relationship('Assign_to')
 


class Map_reviewer(Base):
    __tablename__="map_reviewer"
    map_reviewer=Column(Integer, primary_key=True, index=True)
    reviewer_id=Column(Integer)
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    date=Column(DateTime,default=func.now())     
     
     

class Assign_to(Base):
    __tablename__='assign_to'
    assign_id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    image_id=Column(Integer, ForeignKey('annotation_master.image_id'))
    project_id=Column(Integer,ForeignKey('add_project.project_id'))
    assigned_by=Column(Integer,ForeignKey('user_details.user_id'))
    date_of_assign=Column(DateTime,default=func.now())
   
class Qc_image_map(Base):
    __tablename__='qc_image_map'
    qc_image_map_id=Column(Integer,primary_key=True,index=True)
    image_id=Column(Integer,ForeignKey('annotation_master.image_id'))
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    project_id=Column(Integer,ForeignKey('add_project.project_id'))
    Qc_rejected_date=Column(DateTime,default=func.now())
   
    





class UserMap(Base):
    __tablename__='usermap'
    user_map_id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    created_user_id=Column(Integer, index=True)
    created_date=Column(DateTime, default=func.now())


class Delete_user_map(Base):
    __tablename__='delete_user_map'
    delete_user_map_id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey("user_details.user_id"))
    admin_id=Column(Integer)
    date_of_deletion=Column(DateTime,default=func.now())




class Delete_project_map(Base):
    __tablename__='delete_project_map'
    delete_project_map_id=Column(Integer, primary_key=True, index=True)
    admin_id=Column(Integer,ForeignKey("user_details.user_id"))
    project_id=Column(Integer)
    date_of_deletion=Column(DateTime,default=func.now())


# class Industry(Base):
#     __tablename__= 'industry'
#     industries_id=Column(Integer, primary_key=True, index=True)
#     industry_name=Column(String(255))
#     industry_description=Column(String(255))
#     user_id=Column(Integer, ForeignKey('user_details.user_id'))
    

    
    # User_industry=relationship("User_details")
    


class Add_project(Base):
     __tablename__='add_project'
    
     project_id=Column(Integer,primary_key=True, index=True)
     user_id=Column(Integer,ForeignKey('user_details.user_id'))
     project_name=Column(String(255))
     project_path=Column(String(255))
     industries_name=Column(String(255))
     description=Column(String(255))
     start_date=Column(DateTime)
     enddate=Column(DateTime)
     is_active=Column(Boolean,default=True)
     approved_status=Column(Boolean,default=False)
     approved_by=Column(String(255))


     
     proj_rel=relationship('Add_classes')
     image_proj=relationship('Image_annotation_mapping')
     user=relationship('User_details',back_populates='qc_user')
     inside_map=relationship('Project_inside_folder_map')
     qc_map=relationship('Qc_image_map')



class Project_inside_folder_map(Base):
    __tablename__='project_inside_folder_map'
    inside_folder_map_id=Column(Integer,primary_key=True,index=True)
    related_project_id=Column(Integer,ForeignKey('add_project.project_id'))
    folder_path=Column(String(255))
    date_created=Column(DateTime,default=func.now())



class Project_status(Base):
    __tablename__='project_status'
    project_status_id=Column(Integer,primary_key=True,index=True)
    all_counts=Column(Integer)
    started_count=Column(Integer)
    approved_count=Column(Integer)
    completed_count=Column(Integer)



class Image_annotation_mapping(Base):
    __tablename__='image_annotation_mapping'

    image_annotation_mapping_id=Column(Integer,primary_key=True, index=True)
    image_id=Column(Integer, ForeignKey('annotation_master.image_id'))
    project_id=Column(Integer,ForeignKey('add_project.project_id'))
    bounding_boxes=Column(JSON)
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    class_id=Column(Integer,ForeignKey('add_classes.class_id'))

    

class Add_classes(Base):
    __tablename__='add_classes'
    class_id=Column(Integer, primary_key=True, index=True)
    class_name=Column(String(255))
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    project_id=Column(Integer,ForeignKey('add_project.project_id'))



    class_indus=relationship("Image_annotation_mapping")

class Map_user(Base):
    __tablename__='map_user'
    map_user_id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user_details.user_id"))
    admin_id=Column(Integer)  
    date_created=Column(DateTime,default=func.now())
  


class QC_Assigned(Base):
    __tablename__='qc_assigned'
    qc_User_id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey('user_details.user_id'))
    description=Column(String(255))
    date_created=Column(DateTime,default=func.now())
    status=Column(Boolean,default=False )
    date_Completed=Column(DateTime, default=func.now())
    
# class Backup_User(Base):
#     __tablename__='backup_user'
#     user_id=Column(Integer, primary_key=True)
#     first_name=Column(String(255))
#     last_name=Column(String(255))
#     email=Column(String(255))
#     phone_no=Column(Integer)
#     password=Column(String(255))
#     is_admin=Column(Boolean) 

  
  






class Roles(Base):
    __tablename__='roles'
    roles_id=Column(Integer,primary_key=True,index=True)
    roles_name=Column(String(255))
    roles_description=Column(String(255))    
    date_created=Column(DateTime, default=func.now())
   
    user_role=relationship('User_details')

class User_details(Base):
    __tablename__='user_details'
        
    user_id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String(255))
    last_name=Column(String(255))
    email=Column(String(255))
    phone_no=Column(Integer)
    password=Column(String(255))
    roles_id=Column(Integer,ForeignKey('roles.roles_id'))
    is_active=Column(Boolean,default=True)
    organisation_name=Column(String(255))

    proj_user=relationship("QC_Assigned")
    qc_user=relationship('Add_project')
    class_user=relationship("Add_classes")
    # assign_user_map=relationship("Industry")
    Annotation_master=relationship('Annotation_master')
    Image_annotation_map=relationship('Image_annotation_mapping')
    del_project_mapping=relationship("Delete_project_map")
    qc_image_map=relationship("Qc_image_map")
    reviewer_rel=relationship("Map_reviewer")
    # user_rel=relationship('Assign_to')

  


    

class Shapebox(Base):
    __tablename__='shapebox'
    shapebox_id=Column(Integer,primary_key=True, index=True)
    shapebox_name=Column(String(255))
    
    







    

