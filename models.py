

class Group:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Group(name={self.name})"



class Student: 
    def __init__(self, data):
        self.matricule = data['matricule']
        self.fromG = data['fromG']
        self.toG = data['toG']
        self.priority = data['priority']

    def __repr__(self):
        return f"Student(matricule={self.matricule}, fromG={self.fromG.name}, toG={self.toG.name}, priority={self.priority})"

