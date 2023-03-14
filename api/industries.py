# from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, status, Form
# from starlette.responses import JSONResponse
# from sqlalchemy.orm import Session
# import re
# from datetime import datetime, timedelta
# from typing import Union
# import schema.Industries

# from database import SessionLocal, engine
# import models
# import database
# import sys
# # from utils.utils import _load_model
# import sqlalchemy.exc
# # import uvicorn

# # from pydantic import dict

# import sys

# sys.path.append("..")





# router = APIRouter(prefix='/add_industry', tags=['add_industry'])


# @router.post('/Add_industry')
# async def add_industry(request: Request, add_industry: schema.Industries.Industries, db: Session = Depends(database.get_db)):
#     try:   
#         add_industry_model = models.Industry()
#         # add_industry_model.industries_id=add_industry.industries_id
#         add_industry_model.industry_name=add_industry.industry_name
#         add_industry_model.industry_description = add_industry.industry_description
        
    
#         db.add(add_industry_model)
#         db.commit()
    
#         return JSONResponse(status_code=201, content='industry created successfully')
#     except sqlalchemy.exc.OperationalError:
#         print('some error occured')
#         return JSONResponse(status_code=400, content='some unexpected error occurred')



# @router.get('/all_industries')
# async def get_all_industry( db: Session = Depends(database.get_db)):
#     # projects = db.query(models.Add_project).all()
#     industry=db.query(models.Industry).all()
#     # for industries in industry:
#     #     print(industry.industry_name)
#     # # print(">>>>>>>>>>>>>>>>>>" ,industries)
#     if industry is None:
#         return JSONResponse(status_code=404, content='No industry found with this id')
#     return industry


# @router.get('/{industries_id}', response_model=schema.Industries.Industries)
# async def get_industry_by_id(industries_id: int, db: Session = Depends(database.get_db)):
#     industry = db.query(models.Industry).filter(models.Industry.industries_id == industries_id).first()
#     if industry is None:
#         return JSONResponse(status_code=404, content='No industry found with this id')
#     return industry



# @router.delete('/delete/{industries_id}')
# async def delete_industry(industries_id: int, db: Session = Depends(database.get_db)):
#     try:
#         delete = db.query(models.Industry).filter(models.Industry.industries_id == industries_id).delete()
#         db.commit()
#         if delete:
#             return JSONResponse(status_code=200, content='industry deleted successfully')
#         return JSONResponse(status_code=404, content='No industry found')
#     except sqlalchemy.exc.OperationalError:
#         print(f'error occurred while deleting industry with {industries_id} id')
#         return JSONResponse(status_code=503, content='unexpected error occurred')