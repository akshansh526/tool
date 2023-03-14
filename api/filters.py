

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
import models
import schema.Project, schema.User, schema.Upload_images, schema.Classes
import database





router = APIRouter(prefix="/filter_projects", tags=["filter_projects"])


@router.get("/filter_projects_name/{user_id}", response_model=List[schema.Project.ProjectFilter])
async def filter_projects(
    user_id: int,
    filters: schema.Project.ProjectFilter,
    db: Session = Depends(database.get_db),
):
    print("==========+++++++++++++", filters.__dict__)

    filter_data = (
        db.query(models.Add_project)
        .filter_if(
            filters.start_date is not None,
            models.Add_project.start_date == filters.start_date,
        )
        .filter_if(
            filters.user_id is not None, models.User_details.user_id == filters.user_id
        )
        .filter_if(
            filters.project_id is not None,
            models.Add_project.project_id == filters.project_id,
        )
        .filter_if(
            filters.project_name is not None,
            models.Add_project.project_name == filters.project_name,
        )
        .all()
    )
    print("**********************", filter_data)

    return filter_data


