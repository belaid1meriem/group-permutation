from enum import Enum

class Group(Enum):
    G01 = 1
    G02 = 2
    G03 = 3
    G04 = 4
    G05 = 5
    G06 = 6
    G07 = 7
    G08 = 8
    G09 = 9
    G10 = 10
    

class Student: 
    def __init__(self, matricule: int, fromG: Group, toG: Group, priority: int):
        self.matricule = matricule
        self.fromG = fromG
        self.toG = toG
        self.priority = priority

    def __repr__(self):
        return f"Student(matricule={self.matricule}, fromG={self.fromG.name}, toG={self.toG.name}, priority={self.priority})"

