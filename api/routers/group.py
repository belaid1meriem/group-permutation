from typing import List
from fastapi import APIRouter, Body

from ..schemas.group import GroupPermutationRequest
from ..schemas.student import Student, StudentResponse
from ..services.group_service import process_group_permutation

router = APIRouter()

@router.post(
    "/group_permutation",
    # request_model=GroupPermutationRequest,
    response_model=List[StudentResponse],
    summary="Generate student group permutations",
    description="Takes a list of students and groups to process their movement.",
)
def group_permutation(request: GroupPermutationRequest):
    return process_group_permutation(request.students_list, request.group_list)