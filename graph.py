from igraph import  plot
from views import group_permutation, generate_graph, from_dict_to_students, create_group_list


group_list = ['G01', 'G02', 'G03','G04','G05']
groups = create_group_list(group_list)
print(groups)
students_data = [
    {"matricule": "22/01", "fromG": "G01", "toG": "G02", "date": "2025-02-28 14:30:45.123456"},
    {"matricule": "22/02", "fromG": "G02", "toG": "G03", "date": "2025-02-28 14:31:10.654321"},
    {"matricule": "22/03", "fromG": "G03", "toG": "G04", "date": "2025-02-28 14:32:05.987654"},
    {"matricule": "22/04", "fromG": "G04", "toG": "G01", "date": "2025-02-28 14:33:20.111222"},
    {"matricule": "22/05", "fromG": "G04", "toG": "G05", "date": "2025-02-28 14:34:15.333444"},
    {"matricule": "22/06", "fromG": "G05", "toG": "G04", "date": "2025-02-28 14:35:50.555666"},
]

students = from_dict_to_students(students_data, groups)
print(students)


g, priorities = generate_graph(groups=groups,students=students)    
# Visualize
plot(g,"graph.png", vertex_label=g.vs['label'], edge_label=g.es["label"], edge_arrow_size=1, vertex_size=30)   
group_permutation(g, priorities)
       
        