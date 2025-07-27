from pydantic import BaseModel, Field
from datetime import datetime

class Student(BaseModel):
    matricule: str = Field(..., example="22/0008")
    fromG: str = Field(..., example="G01")
    toG: str = Field(..., example="G02")
    date: datetime  = Field(..., example=datetime.now())
    
class StudentResponse(BaseModel):
    matricule: str = Field(..., example="22/0008")
    fromG: str = Field(..., example="G01")
    toG: str = Field(..., example="G02")
