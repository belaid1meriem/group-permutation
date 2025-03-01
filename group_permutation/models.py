class Group:
    """
    Represents a group with a name and a numerical value.
    
    Attributes:
        name (str): The name of the group.
        value (int): A numerical value associated with the group.
    """
    
    def __init__(self, name: str, value: int):
        """
        Initializes a Group instance.
        
        Args:
            name (str): The name of the group.
            value (int): A numerical value representing the group.
        """
        self.name = name
        self.value = value

    def __repr__(self):
        """
        Returns a string representation of the Group instance.
        
        Returns:
            str: A formatted string representing the group.
        """
        return f"Group(name={self.name})"


class Student:
    """
    Represents a student with information about their matricule, initial group, target group, and priority.
    
    Attributes:
        matricule (str): The student's unique identification number.
        fromG (Group): The group the student is moving from.
        toG (Group): The group the student wants to move to.
        priority (int): The priority level of the student's request.
    """
    
    def __init__(self, data: dict):
        """
        Initializes a Student instance.
        
        Args:
            data (dict): A dictionary containing student details.
                - 'matricule' (str): The student's ID.
                - 'fromG' (Group): The current group.
                - 'toG' (Group): The desired group.
                - 'priority' (int): The priority of the request.
        """
        self.matricule = data['matricule']
        self.fromG = data['fromG']
        self.toG = data['toG']
        self.priority = data['priority']

    def __repr__(self):
        """
        Returns a string representation of the Student instance.
        
        Returns:
            str: A formatted string representing the student.
        """
        return f"Student(matricule={self.matricule}, fromG={self.fromG.name}, toG={self.toG.name}, priority={self.priority})"
