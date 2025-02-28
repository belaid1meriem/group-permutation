from igraph import  plot
from views import get_accepted_students, group_permutation, generate_graph, from_dict_to_students, create_group_list


group_list = ['G01', 'G02', 'G03','G04','G05', 'G06']
groups = create_group_list(group_list)

students_data = [
    {"matricule": "22/01", "fromG": "G01", "toG": "G02", "date": "2025-02-28 14:30:45.123456"},
    {"matricule": "22/02", "fromG": "G02", "toG": "G03", "date": "2025-02-28 14:31:10.654321"},
    {"matricule": "22/03", "fromG": "G03", "toG": "G04", "date": "2025-02-28 14:32:05.987654"},
    {"matricule": "22/04", "fromG": "G04", "toG": "G01", "date": "2025-02-28 14:33:20.111222"},
    
    {"matricule": "22/05", "fromG": "G04", "toG": "G05", "date": "2025-02-28 14:34:15.333444"},
    {"matricule": "22/06", "fromG": "G05", "toG": "G04", "date": "2025-02-28 14:35:50.555666"},
    
    {"matricule": "22/07", "fromG": "G02", "toG": "G06", "date": "2025-02-28 14:36:30.777888"},
    {"matricule": "22/08", "fromG": "G06", "toG": "G03", "date": "2025-02-28 14:37:15.999000"},
    
    {"matricule": "22/09", "fromG": "G01", "toG": "G06", "date": "2025-02-28 14:38:20.123456"},
    {"matricule": "22/10", "fromG": "G06", "toG": "G04", "date": "2025-02-28 14:39:10.654321"},
    
    {"matricule": "22/11", "fromG": "G05", "toG": "G06", "date": "2025-02-28 14:40:45.987654"},
    {"matricule": "22/12", "fromG": "G06", "toG": "G05", "date": "2025-02-28 14:41:50.111222"},
]


students = from_dict_to_students(students_data, groups)



g, priorities = generate_graph(groups=groups,students=students)    

# Visualize
plot(g,"graph.png", vertex_label=g.vs['label'], edge_label=g.es["label"], edge_arrow_size=1, vertex_size=30)  

 
permutations = group_permutation(g, priorities)
print(permutations)
for vertex_stack in permutations:
    print([v['label'] for v in vertex_stack ])


accepted_students = get_accepted_students(g=g, permutations=permutations, students=students)

for student in accepted_students:
    print(student.matricule, student.fromG.name, student.toG.name, student.priority)