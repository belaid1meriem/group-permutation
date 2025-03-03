from typing import List
from fastapi import FastAPI

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from group_permutation import views


app = FastAPI()

from schemas.student import Student, Student_out



@app.post("/group_permutation", response_model=List[Student_out])
def group_permutation(students_list: List[Student], group_list: List[str]):
    groups = views.create_group_list(group_list)
    students_list = [student.model_dump() for student in students_list]
    students = views.from_dict_to_students(students_list, groups)
    
    
    g, priorities = views.generate_graph(groups=groups,students=students)    
    permutations, accepted_students = views.group_permutation(g)
    students = views.get_accepted_students(students_edges=accepted_students, students=students)
    
    accepted_students = []
    for student in students:
        student_dict = {
            "matricule": student.matricule,
            "fromG": student.fromG.name,
            "toG": student.toG.name
        }
        accepted_students.append(Student_out.model_validate(student_dict))
        
    return accepted_students



