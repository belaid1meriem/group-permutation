from ..schemas.student import Student
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List
from .student import Student

class GroupPermutationRequest(BaseModel):
    students_list: List[Student] = Field(..., min_items=1,
        example=[
            {
                "matricule": "22/0008",
                "fromG": "G01",
                "toG": "G02",
                "date": "2025-03-03T10:39:58.392260"
            },
            {
                "matricule": "22/0010",
                "fromG": "G03",
                "toG": "G04",
                "date": "2025-03-03T11:15:20.123456"
            }
        ]
    )
    group_list: List[str] = Field(
        ..., 
        min_items=2,  # At least two groups are required for permutation
        example=["G01", "G02", "G03", "G04"]
    )
    
    @field_validator('group_list')
    @classmethod
    def validate_unique_groups(cls, v: List[str]) -> List[str]:
        """Ensure all groups are unique"""
        # Clean whitespace
        cleaned = [group.strip() for group in v if group.strip()]
        
        # Check for duplicates
        if len(cleaned) != len(set(cleaned)):
            duplicates = [group for group in set(cleaned) if cleaned.count(group) > 1]
            raise ValueError(f'Duplicate groups not allowed: {duplicates}')
        
        return cleaned
    
    @field_validator('students_list')
    @classmethod
    def validate_unique_students(cls, v: List[Student]) -> List[Student]:
        """Ensure each student appears only once in the request"""
        matricules = [student.matricule for student in v]
        
        if len(matricules) != len(set(matricules)):
            # Find duplicates
            duplicates = []
            seen = set()
            for matricule in matricules:
                if matricule in seen:
                    duplicates.append(matricule)
                seen.add(matricule)
            
            raise ValueError(
                f'Duplicate student matricules not allowed: {list(set(duplicates))}. '
                'Each student can only have one group change request.'
            )
        
        return v
    