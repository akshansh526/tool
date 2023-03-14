from pydantic import BaseModel
import datetime

class Qc_assign(BaseModel):
    user_id:int
    date_created:datetime.time
    class Config:
        orm_mode=True


        
