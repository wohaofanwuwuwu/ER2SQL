class Node():
    def __init__(self) -> None:
        self.x=0
        self.y=0
        self.type = "default"
        self.name = ""
    def __init__(self,x,y,type,name="") -> None:
        self.x= x
        self.y =y
        self.type = type
        self.name = name
        
    def set_name(self,name):
        self.name = name

class Edge():
    def __init__(self,node1,node2) -> None:
        self.from_node = node1
        self.to_node   = node2
        self.name = "1"
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
    def add_relation(self,obj):
        if self.object1 == "":
            self.object1 = obj
        else:
            self.object2 = obj 
class SQL_Attribute():
    def __init__(self,name) -> None:
        self.name = name
class SQL_Table():
    def __init__(self,name,pos) -> None:
        self.name = name
        self.str_pos = pos
        self.attribute_names = []
        self.relation_names = []