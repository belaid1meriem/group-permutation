from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


class Student(BaseModel):
    matricule: str = Field(
        ..., 
        example="22/0008",
        unique=True,
        description="Student ID"
    )
    fromG: str = Field(
        ..., 
        min_length=1, 
        max_length=10,
        example="G01",
        description="Source group"
    )
    toG: str = Field(
        ..., 
        min_length=1, 
        max_length=10,
        example="G02",
        description="Destination group"
    )
    date: datetime = Field(
        ..., 
        example=datetime.now(),
        description="Request submission date"
    )
    
    @field_validator('fromG', 'toG')
    @classmethod
    def validate_group_format(cls, v: str) -> str:
        """Validate group names are not empty"""
        v = v.strip()
        if not v:
            raise ValueError('Group name cannot be empty or whitespace')

        return v
    
    @field_validator('date')
    @classmethod
    def validate_date_not_future(cls, v: datetime) -> datetime:
        """Ensure date is not in the future"""
        if v > datetime.now():
            raise ValueError('Request date cannot be in the future')
        return v
    
    @field_validator('date')
    @classmethod
    def validate_date_reasonable(cls, v: datetime) -> datetime:
        """Ensure date is within reasonable bounds (not too old)"""
        # Optional: Reject dates older than 1 year
        from datetime import timedelta
        one_year_ago = datetime.now() - timedelta(days=365)
        
        if v < one_year_ago:
            raise ValueError('Request date cannot be older than 1 year')
        
        return v
    
    @model_validator(mode='after')
    def validate_different_groups(self) -> 'Student':
        """Ensure student is not trying to move to the same group"""
        if self.fromG == self.toG:
            raise ValueError(
                f'Source group ({self.fromG}) and destination group ({self.toG}) cannot be the same. '
                'Student is already in the desired group.'
            )
        return self
    
    
class StudentResponse(BaseModel):
    matricule: str = Field(..., min_length=1, example="22/0008")
    fromG: str = Field(..., min_length=1, example="G01")
    toG: str = Field(..., min_length=1, example="G02")
