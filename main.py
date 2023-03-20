




import uvicorn
from fastapi import  FastAPI



from database import  SessionLocal, engine
import models

# from schema import Filters
from api import add_project, filters,add_classes,upload_images,del_project,assign,auth,filters,annotation_map,shapebox,roles
from api import all_details,new_filter,search
from fastapi.middleware.cors import CORSMiddleware




tool = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme":"obsidian"})








def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
       "http://localhost",
    "http://192.168.1.118:4200",
    
]

tool.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    # allow_methods=["POST","GET","OPTIONS"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)



tool.include_router(auth.router)
tool.include_router(add_project.router)
tool.include_router(add_classes.router)
tool.include_router(upload_images.router)
tool.include_router(del_project.router)
tool.include_router(assign.router)
tool.include_router(filters.router)
tool.include_router(annotation_map.router)
tool.include_router(shapebox.router)
tool.include_router(roles.router)
# tool.include_router(current_user.router)
tool.include_router(all_details.router)
tool.include_router(search.router)
# tool.include_router(authlog.router)

if __name__ == "__main__":
    uvicorn.run("main:tool", port=5000,reload=True)  