from igraph import Graph, Vertex, Edge
from igraph import Graph
from .models import Group, Student


def create_group_list(groups: list[str]) -> list[Group]:
    """
    Creates a list of Group instances from a list of group names.
    
    Args:
        groups (list[str]): A list of group names.
    
    Returns:
        list[Group]: A list of Group objects with assigned values based on their index.
    """
    groups_list = []
    for i, group in enumerate(groups):
        groups_list.append(Group(group, i))
    return groups_list

def get_group_by_name(groups: list[Group], name: str) -> Group:
    """
    Retrieves a Group instance by its name from a list of groups.
    
    Args:
        groups (list[Group]): A list of Group instances.
        name (str): The name of the group to retrieve.
    
    Returns:
        Group: The matching Group instance.
    
    Raises:
        ValueError: If the group with the specified name does not exist.
    """
    for group in groups:
        if group.name == name:
            return group
    raise ValueError("Group does not exist")


def calculate_prio(students: list[dict]) -> list[dict]:
    """
    Calculates priority for a list of students based on their date.
    
    Args:
        students (list[dict]): A list of dictionaries representing students. Each dictionary must contain a 'date' key.
    
    Returns:
        list[dict]: The updated list of students with assigned priority values.
    """
    students = sorted(students, key=lambda student: student['date'])
    for i, student in enumerate(students):
        student['priority'] = i + 1
    return students


def from_dict_to_students(data: list[dict], groups: list[Group]) -> list[Student]:
    """
    Converts a list of student dictionaries into a list of Student instances.
    
    Args:
        data (list[dict]): A list of dictionaries containing student data.
        groups (list[Group]): A list of available Group instances.
    
    Returns:
        list[Student]: A list of Student instances with assigned groups and priorities.
    """
    students = []
    data = calculate_prio(data)
    for student in data:
        student['fromG'] = get_group_by_name(groups, student['fromG'])
        student['toG'] = get_group_by_name(groups, student['toG'])
        students.append(Student(student))
    return students


def generate_graph_edges(students: list[Student], groups: list[Group]):
    """
    Generates graph edges representing student movements between groups.
    
    Args:
        students (list[Student]): A list of Student instances.
        groups (list[Group]): A list of Group instances.
    
    Returns:
        tuple: A tuple containing four lists:
            - edge_list (list[tuple[int, int]]): List of edges representing movements between groups.
            - labels (list[int]): Labels representing student priorities.
            - priorities (list[int]): List of student priority values.
            - matricules (list[str]): List of student matricule IDs.
    """
    edge_list = []
    labels = []
    priorities = []
    matricules = []
    
    for student in students:
        edge_list.append((groups.index(student.fromG), groups.index(student.toG)))
        priorities.append(student.priority)
        labels.append(student.priority)
        matricules.append(student.matricule)
        
    return edge_list, labels, priorities, matricules




def generate_graph(groups: list[Group], students: list[Student]):
    """
    Generates an igraph graph from the given groups and students.
    
    Args:
        groups (list[Group]): A list of Group instances.
        students (list[Student]): A list of Student instances.
    
    Returns:
        tuple: A tuple containing:
            - g (Graph): The generated directed graph with vertices and edges.
            - priorities (list[int]): List of student priority values.
    """
    g = Graph(directed=True)
    g.add_vertices(len(groups))  
    g.vs['label'] = [group.name for group in groups]
    edges_list, labels, priorities, matricules = generate_graph_edges(students=students, groups=groups)
    g.add_edges(edges_list)  
    g.es['label'] = labels
    g.es['priority'] = priorities
    g.es['matricules'] = matricules
    g.es['used'] = [False] * len(edges_list)
    g.es['retained'] = [False] * len(edges_list)
    g.es['removed'] = [False] * len(edges_list)
    return g, priorities




def start_vertex(g: Graph) -> Vertex | None:
    """
    Finds the vertex with the minimum priority edge.
    
    Args:
        g (Graph): The input directed graph.
    
    Returns:
        Vertex | None: The vertex with the minimum priority edge, or None if no edges are available.
    """
    unused_edges = g.es.select(used=False)
    if not unused_edges:
        return None  # No valid starting vertex
    min_priority_edge = min(unused_edges, key=lambda e: e['priority'])
    return g.vs[min_priority_edge.source]




def find_min_prio_edge(g: Graph, v: Vertex):
    """
    Finds the outgoing edge of v with the minimum priority.
    
    Args:
        g (Graph): The input directed graph.
        v (Vertex): The vertex for which to find the minimum priority outgoing edge.
    
    Returns:
        Edge | None: The outgoing edge with the minimum priority, or None if no valid edge exists.
    """
    outgoing_edges = g.es.select([e.index for e in v.incident(mode='out') if not g.es[e.index]['used']])
    
    if not outgoing_edges:  # No outgoing edges
        return None
    
    return min(outgoing_edges, key=lambda e: e["priority"])






def correcting_used_retained_labels(g: Graph):
    """
    Resets the 'used' attribute for edges that are neither retained nor removed.
    
    Args:
        g (Graph): The input directed graph.
    """
    for e in g.es:
        if not e['retained'] and e['used'] and not e['removed']:
            e['used'] = False
            
            
            
def best_circuit_search(g: Graph) -> list[list[Edge], list[Vertex]]:
    """
    Searches for the best circuit in the graph using priority-based traversal.
    
    Args:
        g (Graph): The input directed graph.
    
    Returns:
        tuple: A tuple containing two lists:
            - A list of edges forming the best circuit.
            - A list of vertices in the traversal order.
    """
    correcting_used_retained_labels(g)
    
    start = start_vertex(g)
    if start is None:  # No valid starting point
        return [], []

    vertex_stack = [start]
    edge_stack = []
    
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        next_edge = find_min_prio_edge(g, current_vertex)

        if next_edge:
            next_vertex = g.vs[next_edge.target]    
            vertex_stack.append(next_vertex)
            
            next_edge['used'] = True
            next_edge['retained'] = True
            edge_stack.append(next_edge)
            
        elif current_vertex == start:
            if len(edge_stack) == 0:
                outgoing_edges = g.es.select([e.index for e in current_vertex.incident(mode='out') if not g.es[e.index]['retained']])

                if outgoing_edges:
                    min_edge = min(outgoing_edges, key=lambda e: e['priority'])
                    min_edge['removed'] = True
                    
            break
        else:
            vertex_stack.pop()
            edge = edge_stack.pop()
            g.es[edge.index]['retained'] = False
            
    return vertex_stack, edge_stack


def group_permutation(g: Graph) -> list[list[list[Vertex]], list[list[Edge]]]:
    """
    Finds all possible group permutations based on available paths in the graph.
    
    Args:
        g (Graph): The input directed graph.
    
    Returns:
        tuple: A tuple containing two lists:
            - permutations (list[list[Vertex]]): A list of vertex group permutations.
            - students (list[list[Edge]]): A list of edge-based student movements.
    """
    permutations = []
    students = []
    
    while g.es.select(used=False):
        vertex_stack, edge_stack = best_circuit_search(g)
        permutations.append(vertex_stack)
        if len(edge_stack):
            students.append(edge_stack)
        
    return permutations, students



def get_accepted_students(students_edges: list[list[Edge]], students: list[Student]) -> list[Student]:
    """
    Retrieves the students whose movement requests have been accepted.
    
    Args:
        students_edges (list[list[Edge]]): A list of lists containing accepted edges representing student movements.
        students (list[Student]): A list of all students.
    
    Returns:
        list[Student]: A list of students whose requests have been accepted.
    """
    student_map = {s.matricule: s for s in students}
    accepted_students = [student_map[edge['matricules']] for edge_stack in students_edges for edge in edge_stack if edge['matricules'] in student_map]
    return accepted_students
