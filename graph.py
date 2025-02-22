from igraph import Graph, plot, Vertex, Edge
from models import Group, Student

# students = [
#     Student(matricule=1, fromG=Group.G01, toG=Group.G02, priority=1),
#     Student(matricule=2, fromG=Group.G02, toG=Group.G03, priority=2),
#     Student(matricule=3, fromG=Group.G03, toG=Group.G01, priority=3),
#     Student(matricule=4, fromG=Group.G01, toG=Group.G04, priority=4),
#     Student(matricule=5, fromG=Group.G04, toG=Group.G02, priority=5),
#     Student(matricule=6, fromG=Group.G07, toG=Group.G08, priority=6),
#     Student(matricule=7, fromG=Group.G09, toG=Group.G08, priority=7),
#     Student(matricule=8, fromG=Group.G01, toG=Group.G05, priority=8),
#     Student(matricule=9, fromG=Group.G03, toG=Group.G06, priority=9),
#     Student(matricule=10, fromG=Group.G02, toG=Group.G07, priority=10),
# ]

# students = [
#     Student(matricule=1, fromG=Group.G01, toG=Group.G02, priority=1),
#     Student(matricule=2, fromG=Group.G02, toG=Group.G03, priority=2),
#     Student(matricule=3, fromG=Group.G03, toG=Group.G04, priority=3),
#     Student(matricule=4, fromG=Group.G04, toG=Group.G05, priority=4),
#     Student(matricule=5, fromG=Group.G05, toG=Group.G06, priority=5),
#     Student(matricule=6, fromG=Group.G06, toG=Group.G01, priority=6),  # Cycle back to G01
# ]

# students = [
#     Student(matricule=1, fromG=Group.G01, toG=Group.G02, priority=1),
#     Student(matricule=2, fromG=Group.G02, toG=Group.G03, priority=2),
#     Student(matricule=3, fromG=Group.G05, toG=Group.G06, priority=3),  # Separate cluster
#     Student(matricule=4, fromG=Group.G06, toG=Group.G07, priority=4),  # Separate cluster
#     Student(matricule=5, fromG=Group.G08, toG=Group.G09, priority=5),  # Isolated movement
# ]

# students = [
#     Student(matricule=1, fromG=Group.G01, toG=Group.G05, priority=1),
#     Student(matricule=2, fromG=Group.G02, toG=Group.G05, priority=2),
#     Student(matricule=3, fromG=Group.G03, toG=Group.G05, priority=3),
#     Student(matricule=4, fromG=Group.G04, toG=Group.G05, priority=4),
#     Student(matricule=5, fromG=Group.G06, toG=Group.G07, priority=5),
# ]

# students = [
#     Student(matricule=1, fromG=Group.G01, toG=Group.G02, priority=5),
#     Student(matricule=2, fromG=Group.G02, toG=Group.G03, priority=1),
#     Student(matricule=3, fromG=Group.G03, toG=Group.G04, priority=8),
#     Student(matricule=4, fromG=Group.G04, toG=Group.G05, priority=3),
#     Student(matricule=5, fromG=Group.G05, toG=Group.G06, priority=7),
#     Student(matricule=6, fromG=Group.G06, toG=Group.G01, priority=2),
# ]

# students = [
#     Student(matricule=1, fromG=Group.G01, toG=Group.G02, priority=2),
#     Student(matricule=2, fromG=Group.G02, toG=Group.G03, priority=3),
#     Student(matricule=3, fromG=Group.G03, toG=Group.G04, priority=1),
#     Student(matricule=4, fromG=Group.G04, toG=Group.G01, priority=4),  # Cycle 1: G01 → G02 → G03 → G04 → G01
    
#     Student(matricule=5, fromG=Group.G05, toG=Group.G06, priority=5),
#     Student(matricule=6, fromG=Group.G06, toG=Group.G07, priority=6),
#     Student(matricule=7, fromG=Group.G07, toG=Group.G05, priority=2),  # Cycle 2: G05 → G06 → G07 → G05
    
#     Student(matricule=8, fromG=Group.G04, toG=Group.G06, priority=7),  # Link between cycles
#     Student(matricule=9, fromG=Group.G07, toG=Group.G02, priority=8),  # Another interlink
# ]

students = [
    Student(matricule=1, fromG=Group.G01, toG=Group.G05, priority=1),
    Student(matricule=2, fromG=Group.G02, toG=Group.G05, priority=2),
    Student(matricule=3, fromG=Group.G03, toG=Group.G05, priority=3),
    Student(matricule=4, fromG=Group.G04, toG=Group.G05, priority=4),  # G05 is the bottleneck (many entering)
    
    Student(matricule=5, fromG=Group.G05, toG=Group.G06, priority=5),
    Student(matricule=6, fromG=Group.G06, toG=Group.G07, priority=6),
    Student(matricule=7, fromG=Group.G07, toG=Group.G08, priority=7),  # G08 is a **dead-end**
    
    Student(matricule=8, fromG=Group.G09, toG=Group.G10, priority=8),  # Disconnected subgraph
    Student(matricule=9, fromG=Group.G10, toG=Group.G09, priority=9),  # Small cycle in a separate component
]







groups = list(map(lambda group: group.name, Group))

# Create a directed graph 
g = Graph(directed=True)
g.add_vertices(len(groups))  
g.vs['label'] = groups
def edges (students: list[Student], groups: list[Group]) :
    edge_list= []
    labels = [] 
    priorities = []
    for student in students :
        edge_list.append((groups.index(student.fromG.name), groups.index(student.toG.name)))
        priorities.append(student.priority)
        labels.append(student.priority)
    return edge_list, labels, priorities

edges_list, labels, priorities = edges(students=students, groups=groups)
g.add_edges(edges_list)  
g.es['label'] = labels
g.es['priority'] = priorities
# g.es['state'] = ['unused'] * len(students)
# Visualize
plot(g,"graph.png", vertex_label=g.vs['label'], edge_label=g.es["label"], edge_arrow_size=1, vertex_size=30)



def start_vertex(g: Graph, priorities: list[int]):
    return g.vs[ g.es.find(priority= min(priorities)).source ]

def find_min_prio_edge(g: Graph, v: Vertex):
    """Finds the outgoing edge of v with the minimum priority."""
    outgoing_edges = g.es[[e.index for e in v.incident(mode='out')]]

    if not outgoing_edges:  # No outgoing edges
        return None
    
    # Get priorities of outgoing edges
    edge_priorities = [e["priority"] for e in outgoing_edges]
    
    # Find the minimum priority among these edges
    min_priority = min(edge_priorities)

    return outgoing_edges.find(priority=min_priority)




def best_circuit_search(g: Graph, priorities: list[int]) -> list[Graph, list[Vertex]]:
    g_copy = g.copy()
    start = start_vertex(g_copy, priorities)
    vertex_stack = [start]
    
    while vertex_stack:
        current_vertex= vertex_stack[-1]
        next_edge = find_min_prio_edge(g_copy, current_vertex)
        print(current_vertex)
        print(next_edge)
        if next_edge :
            next_vertex = g_copy.vs[next_edge.target]    
            vertex_stack.append(next_vertex)
            priorities.remove(next_edge['priority'])
            g_copy.delete_edges(next_edge.index)
            
        elif current_vertex == start : 
            break
        else : 
            vertex_stack.pop()
    return g_copy, vertex_stack


def group_permutation(g: Graph, priorities):
    while len(g.es):
        g, vertex_stack= best_circuit_search(g, priorities)
        print([v['label'] for v in vertex_stack])
        
group_permutation(g, priorities)
       
        