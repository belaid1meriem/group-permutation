from typing import List
from schemas.student import Student, Student_out
from group_permutation import views

def process_group_permutation(students_list: List[Student], group_list: List[str]) -> List[Student_out]:
    groups = views.create_group_list(group_list)
    
    students_list = [student.model_dump() for student in students_list]
    students = views.from_dict_to_students(students_list, groups)
    
    g, priorities = views.generate_graph(groups=groups, students=students)    
    permutations, accepted_students = views.group_permutation(g)
    students = views.get_accepted_students(students_edges=accepted_students, students=students)
    
    accepted_students_list = []
    for student in students:
        student_dict = {
            "matricule": student.matricule,
            "fromG": student.fromG.name,
            "toG": student.toG.name
        }
        accepted_students_list.append(Student_out.model_validate(student_dict))
        
    return accepted_students_list
