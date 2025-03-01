from igraph import  plot
from views import get_accepted_students, group_permutation, generate_graph, from_dict_to_students, create_group_list


group_list = ['G01', 'G02', 'G03', 'G04', 'G05', 'G06', 
          'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 
          'G13', 'G14', 'G15']

groups = create_group_list(group_list)

students_data = [
    {"matricule": "22/01", "fromG": "G01", "toG": "G02", "date": "2025-02-28 14:30:45.123456"},
    {"matricule": "22/02", "fromG": "G02", "toG": "G03", "date": "2025-02-28 14:31:10.654321"},
    {"matricule": "22/03", "fromG": "G03", "toG": "G04", "date": "2025-02-28 14:32:05.987654"},
    {"matricule": "22/04", "fromG": "G04", "toG": "G05", "date": "2025-02-28 14:33:20.111222"},
    {"matricule": "22/05", "fromG": "G05", "toG": "G06", "date": "2025-02-28 14:34:15.333444"},
    {"matricule": "22/06", "fromG": "G06", "toG": "G07", "date": "2025-02-28 14:35:50.555666"},
    {"matricule": "22/07", "fromG": "G07", "toG": "G08", "date": "2025-02-28 14:36:30.777888"},
    {"matricule": "22/08", "fromG": "G08", "toG": "G09", "date": "2025-02-28 14:37:15.999000"},
    {"matricule": "22/09", "fromG": "G09", "toG": "G10", "date": "2025-02-28 14:38:20.123456"},
    {"matricule": "22/10", "fromG": "G10", "toG": "G11", "date": "2025-02-28 14:39:10.654321"},
    
    {"matricule": "22/11", "fromG": "G11", "toG": "G12", "date": "2025-02-28 14:40:45.987654"},
    {"matricule": "22/12", "fromG": "G12", "toG": "G13", "date": "2025-02-28 14:41:50.111222"},
    {"matricule": "22/13", "fromG": "G13", "toG": "G14", "date": "2025-02-28 14:42:30.222333"},
    {"matricule": "22/14", "fromG": "G14", "toG": "G15", "date": "2025-02-28 14:43:15.444555"},
    {"matricule": "22/15", "fromG": "G15", "toG": "G01", "date": "2025-02-28 14:44:00.666777"},  # Cycle created
    
    {"matricule": "22/16", "fromG": "G02", "toG": "G10", "date": "2025-02-28 14:45:20.888999"},
    {"matricule": "22/17", "fromG": "G10", "toG": "G07", "date": "2025-02-28 14:46:50.000111"},
    {"matricule": "22/18", "fromG": "G07", "toG": "G05", "date": "2025-02-28 14:47:10.222333"},
    {"matricule": "22/19", "fromG": "G05", "toG": "G13", "date": "2025-02-28 14:48:40.444555"},
    {"matricule": "22/20", "fromG": "G13", "toG": "G02", "date": "2025-02-28 14:49:55.666777"},  # Another cycle
    
    {"matricule": "22/21", "fromG": "G03", "toG": "G15", "date": "2025-02-28 14:50:30.888999"},
    {"matricule": "22/22", "fromG": "G15", "toG": "G06", "date": "2025-02-28 14:51:45.000111"},
    {"matricule": "22/23", "fromG": "G06", "toG": "G12", "date": "2025-02-28 14:52:50.222333"},
    {"matricule": "22/24", "fromG": "G12", "toG": "G08", "date": "2025-02-28 14:53:40.444555"},
    {"matricule": "22/25", "fromG": "G08", "toG": "G04", "date": "2025-02-28 14:54:25.666777"},
    
    {"matricule": "22/26", "fromG": "G14", "toG": "G03", "date": "2025-02-28 14:55:50.888999"},
    {"matricule": "22/27", "fromG": "G04", "toG": "G09", "date": "2025-02-28 14:56:45.000111"},
    {"matricule": "22/28", "fromG": "G09", "toG": "G01", "date": "2025-02-28 14:57:30.222333"},
    {"matricule": "22/29", "fromG": "G01", "toG": "G11", "date": "2025-02-28 14:58:10.444555"},
    {"matricule": "22/30", "fromG": "G11", "toG": "G14", "date": "2025-02-28 14:59:55.666777"},  # Final cycle
]



students = from_dict_to_students(students_data, groups)



g, priorities = generate_graph(groups=groups,students=students)    

# Visualize

# Define an improved plot function
visual_style = {
    "vertex_label": g.vs["label"],      # Show vertex labels
    "vertex_size": 20,                  # Reduce vertex size for better spacing
    "vertex_color": "lightblue",        # Improve visibility
    "vertex_label_size": 10,            # Make vertex labels smaller
    "edge_label": g.es["label"],        # Show edge labels
    "edge_label_size": 8,               # Reduce edge label size
    "edge_arrow_size": 0.7,             # Reduce arrow size to prevent clutter
    "bbox": (1000, 1000),               # Increase plot size
    "margin": 50,                       # Add margin to prevent text clipping
    "layout": g.layout("kk"),           # Use Kamada-Kawai layout for better spacing
}

# Generate the plot
plot(g, "graph.png", **visual_style)

 
permutations, accepted_students = group_permutation(g)

print("Permutations in groups")
for vertex_stack in permutations:
    print([v['label'] for v in vertex_stack ])

# for edge_stack in accepted_students:
#     print([e['matricules'] for e in edge_stack ])

accepted_students = get_accepted_students(students_edges=accepted_students, students=students)

print("Accepted students")
for student in accepted_students:
    print(student.matricule, student.fromG.name, student.toG.name, student.priority)