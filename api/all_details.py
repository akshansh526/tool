from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
import database
import sys
sys.path.append("..")



router = APIRouter(prefix="/get_project", tags=["get_project"])


@router.get("/all_project/{project_id}/{user_id}")
async def get_all_project_by_project_id(project_id: int,user_id:int, db: Session = Depends(database.get_db)):
    project_det = (
        db.query(models.Add_project.project_path)
        .filter(models.Add_project.project_id == project_id)
        .first()
    )
    image_path = (
        db.query(models.Annotation_master.image_url)
        .filter(models.Annotation_master.project_id == project_id)
        .all()
    )
    assign = (
        db.query(models.Assign_to)
        .filter(models.Assign_to.project_id == project_id)
        .first()
    )
    user= (
        db.query(models.User_details)
        .filter(models.User_details.user_id == user_id)
        .first()
    )
    
    # if project_det.__dict__:
    #              return {"projects":project_det,"images":image_path,"assigned":assign,"users":user}
             
    # else:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"image with associated with this project id {project_id} is not found please upload images",)
