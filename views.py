from igraph import Graph, Vertex
from igraph import Graph
from models import Group, Student


def create_group_list(groups: list[str]):
    groups_list = []
    for i, group in enumerate(groups):
        groups_list.append(Group(group, i))
    return groups_list

def get_group_by_name(groups: list[Group], name: str) -> Group:
    for group in groups:
        if group.name == name:
            return group
    raise ValueError("Group does not exist")

def calculate_prio(students: list[dict]):
    students = sorted(students, key=lambda student: student['date'])
    for i, student in enumerate(students):
        student['priority'] = i + 1
    return students

def from_dict_to_students(data: list[dict], groups: list[Group]) -> list[Student]:
    students = []
    data = calculate_prio(data)
    for student in data:
        student['fromG']= get_group_by_name(groups,student['fromG'])
        student['toG']= get_group_by_name(groups, student['toG'])
        print(student['fromG'], student['toG'])
        students.append(Student(student))
    return students


def generate_graph_edges (students: list[Student], groups: list[Group]) :
    
    edge_list= []
    labels = [] 
    priorities = []
    
    for student in students :
        edge_list.append((groups.index(student.fromG), groups.index(student.toG)))
        priorities.append(student.priority)
        labels.append(student.priority)
        
    return edge_list, labels, priorities




def generate_graph(groups: list[Group], students: list[Student]):
    print(groups)
    g = Graph(directed=True)
    g.add_vertices(len(groups))  
    g.vs['label'] = [group.name for group in groups]
    edges_list, labels, priorities = generate_graph_edges(students=students, groups=groups)
    g.add_edges(edges_list)  
    g.es['label'] = labels
    g.es['priority'] = priorities
    
    return g, priorities


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
  