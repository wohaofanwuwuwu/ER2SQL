class Node():
    def __init__(self,x=0,y=0,type="default",name="") -> None:
        self.x= x
        self.y =y
        self.type = type
        self.name = name
        self.iskey = "False"
    def set_name(self,name):
        self.name = name

class Edge():
    def __init__(self,node1,node2) -> None:
        self.from_node = node1
        self.to_node   = node2
        self.name = ""
    def set_name(self,num):
        self.name = num
class Graph():
    def __init__(self) -> None:
        self.nodes = []
        self.edges = []
        self.num = 0
class SQL_Relation():
    def __init__(self,name) -> None:
        self.name = name
        self.object1 = ""
        self.object2 = ""
        self.obj1type = '1'
        self.obj2type = '1'
        self.attributes = []
    def add_relation(self,obj,t):
        if self.object1 == "":
            self.object1 = obj
            self.obj1type = t
        else:
            self.object2 = obj
            self.obj2type = t 
    def add_attribute(self,att):
        self.attributes.append(att)
class SQL_Attribute():
    def __init__(self,name,t) -> None:
        self.name = name
        self.type = t
        self.len = "50"
class SQL_Table():
    def __init__(self,name) -> None:
        self.name = name
        self.key = []
        self.foreign_key =[]
        self.attributes = []
    def add_attribute(self,att):
        self.attributes.append(att)