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
class Graph():
    def __init__(self) -> None:
        self.nodes = []
        self.edges = []
        self.num = 0
