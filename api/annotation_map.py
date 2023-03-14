from fastapi import Depends, APIRouter,status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
import schema.Project
import schema.User
import schema.Annotation
import models
import database
import sys
import sqlalchemy.exc
import sys
from starlette.exceptions import HTTPException
from flask import jsonify
sys.path.append("..")


router = APIRouter(prefix="/map_annotation", tags=["map_annotation"])


def func1(data):
    for key, value in data.items():
        print(str(key) + "->" + str(value))

        if type(value) == type(dict()):
            func1(value)
        elif type(value) == type(dict()):
            for val in value:
                if type(val) == type(str()):
                    pass
                elif type(val) == type(dict()):
                    pass
                else:
                    func1(val)
    print("????????", key, value)

@router.post("/Annotation_map/{project_id}/{user_id}/{image_id}/{class_id}")
async def Mapping_annotations(
    user_id: int,
    Project_id: int,
    image_id: int,
    class_id:int,
    annotation_map: schema.Annotation.Annotation_in,
    db: Session = Depends(database.get_db),
):
    try:
        annotation_model = models.Image_annotation_mapping()
        annotation_model.project_id = Project_id
        annotation_model.user_id = user_id
        annotation_model.image_id = image_id
        annotation_model.class_id = class_id
        annotation_model.bounding_boxes = annotation_map.bounding_box

        db.add(annotation_model)
        db.commit()

        return JSONResponse(status_code=201, content=" annotation stored successfully")
    except sqlalchemy.exc.OperationalError:
        print("some error occured")
        return JSONResponse(status_code=400, content="some unexpected error occurred")


@router.get("/all_annotations/{image_id}")
async def get_all_annotations(image_id: int, db: Session = Depends(database.get_db)):
    annotations = (
        db.query(models.Image_annotation_mapping)
        .filter(models.Image_annotation_mapping.image_id == image_id)
        .all()
    )
    annotations2 = db.query(models.Image_annotation_mapping.bounding_boxes)[-1]
    print("+++++++++", annotations2)
    print(annotations)
    p_list = annotations2

    get_id = p_list[0]
    print("++++++++", get_id)
    func1(get_id)
    print(">>>>>>>>>>>>>>>>>", (get_id))
    if annotations:
                return {"annotations":annotations}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"image with associated with this project id {image_id} is not found please upload images",)

    # if annotations is None:
    #     return JSONResponse(
    #         status_code=404, content="No anonotations found with this id"
    #     )
    # return annotations


@router.get("/get_annotations_by_user/{user_id}")
async def annot_by_user(user_id: int, db: Session = Depends(database.get_db)):
    classes = (
        db.query(models.Image_annotation_mapping)
        .filter(models.Image_annotation_mapping.user_id == user_id)
        .all()
    )
    if classes is None:
        return JSONResponse(status_code=404, content="No project found with this id")
    return classes


@router.delete("/delete/{user_id}")
async def delete_annotations(user_id: int, db: Session = Depends(database.get_db)):
    try:
        delete = (
            db.query(models.Image_annotation_mapping)
            .filter(models.Image_annotation_mapping.user_id == user_id)
            .delete()
        )
        db.commit()
        if delete:
            return JSONResponse(
                status_code=200, content="Annotations deleted successfully"
            )
        return JSONResponse(status_code=404, content="No annotation found")
    except sqlalchemy.exc.OperationalError:
        print(f"error occurred while deleting annotations with {user_id} id")
        return JSONResponse(status_code=503, content="unexpected error occurred")


@router.put('/update_annot/{image_id}')
async def update_annot(image_id:int,update_annot:schema.Annotation.Update_bounding_boxes,db: Session = Depends(database.get_db)):
    try:
       
       annotation={update_annot.Update_bounding_boxes} 

    #    new_path="E:/annotation/Project_datasets/"+project_names[0]
       db.query(models.Image_annotation_mapping).filter(models.Annotation_master.image_id==image_id).update({"bounding_boxes":jsonify(annotation)})
       db.commit()
       return JSONResponse(status_code=201, content='Project created successfully')
    except sqlalchemy.exc.OperationalError:
        print('some error occured')
        return JSONResponse(status_code=400, content='some unexpected error occurred')




@router.post('/qc_rejected_images/{image_id}/{user_id}/{project_id}')
async def qc_rejected_images(image_id:int,user_id:int,project_id:int, db:Session= Depends (database.get_db)):
      qc_model = models.Qc_image_map()
      qc_user_model=models.User_details()
      user_filter=db.query(models.User_details).filter_by(roles_id=1)
      print("user_filter>>>>>>>>>.",user_filter)
      qc_model.image_id=image_id
      qc_model.user_id=user_id
      qc_model.project_id=project_id
      db.add(qc_model)
      
      db.commit() 

      if qc_model:
                 return JSONResponse(status_code=201, content='rejected images sent successfully')
                 
      else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"image with associated with this project id {image_id,user_id,project_id} is not found please upload images",)
      


      
      

