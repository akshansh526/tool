from pydantic import BaseModel

class ShapeBoxIn(BaseModel):
    shapebox_name:str

    class Config:
        orm_mode = True