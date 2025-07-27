from typing import List
from fastapi import APIRouter, Body
from ..schemas.student import Student, StudentResponse
from ..services.group_service import process_group_permutation

router = APIRouter()

@router.post(
    "/group_permutation",
    response_model=List[StudentResponse],
    summary="Generate student group permutations",
    description="Takes a list of students and groups to process their movement.",
)
def group_permutation(
    students_list: List[Student] = Body(
        ...,
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
    ),
    group_list: List[str] = Body(
        ...,
        example=["G01", "G02", "G03", "G04"]
    )
):
    return process_group_permutation(students_list, group_list)