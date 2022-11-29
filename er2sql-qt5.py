import sys
from enum import Enum
from PyQt5 import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QFont, QColor, QPen,QPixmap,QCursor,QPolygon
from PyQt5.QtCore import QSize,QPoint,QPointF,QRect
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, 
                             QAction, QPlainTextEdit, QStyle, QFileDialog,
                             QMessageBox)
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QPushButton,QLineEdit,
    QHBoxLayout, QVBoxLayout,qApp)
from ER_Graph import Node ,Graph,Edge,SQL_Table,SQL_Attribute,SQL_Relation

class cursor_state():
    def __init__(self):
        self.state = "default"
        self.press_state = "False"
        self.x = 0
        self.y = 0
        self.press_position = [0,0] #position relatively offset for screen's left-up corner

class Map_State():
    def __init__(self):
        self.woffset = 0
        self.hoffset = 0
        self.origin_offset=[0,0]#coordinate origin offset to window's left-up corner
        self.horizon_step= 65
        self.vertical_step= 30
class Input_Box(QLineEdit):
    def __init__(self,str,s,node) -> None:
        super().__init__(str,s)
        self.node = node

cursor = cursor_state()
map_state = Map_State()

graph = Graph()
line_edit = ""
link_success = "False"

class main_window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.model = "diagram"
        self.initUI()
        

    def initUI(self):               
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 1000, 600)  
        self.move(300, 300)
        self.setWindowTitle('Simple')
        
        self.initMenuBar() 
        self.initToolBar()
        self.init_center_widget()
        
        self.show()

    def init_center_widget(self):
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        layout = QVBoxLayout()
        self.center_layout = layout
        center_widget.setLayout(layout)
        coordinate_map = Coordinate_Map()
        self.coordinate_map = coordinate_map
        text_box = Text_Box()
        text_box.setReadOnly(True)
        self.text_box = text_box
        self.text_box.setParent(None)
        self.add_widgets(coordinate_map)

    def add_widgets(self,widget):
        self.center_layout.addWidget(widget)
        
    def show_txteditor(self):
        self.txtEditor = QPlainTextEdit(self)  
        self.setCentralWidget(self.txtEditor)

    def initMenuBar(self):
        menuBar = self.menuBar()       
        fileMenu = menuBar.addMenu('文件(&F)')
        changeMenu = menuBar.addMenu('转化(&C)')
        editMenu = menuBar.addMenu('编辑(&E)')
        formatMenu = menuBar.addMenu('模式(&M)')
        helpMenu = menuBar.addMenu('帮助(&H)')

        style = QApplication.style()
        self.new_file(fileMenu,style)
        self.save_file(fileMenu,style)
        self.saveas_file(fileMenu,style)
        self.exchange_vision(changeMenu,style)

    def onFileNew(self):
        pass
    def check_er(self):
        self.text_box.setParent(None)
        self.add_widgets(self.coordinate_map)
        self.update()
        
    def check_sql(self):
        global graph
        self.coordinate_map.setParent(None)
        for edge in graph.edges:
            match edge.from_node.type:
                case "object":
                    table = self.text_box.find_table(edge.from_node.name)
                    if table == "False":
                        table = self.text_box.create_table(edge.from_node.name)   
                    if edge.to_node.type == "attribute":
                        t = "CHAR"
                        att = SQL_Attribute(edge.to_node.name,t)
                        if edge.to_node.iskey == "True":
                            table.key.append(att)
                        table.add_attribute(att)
                    if edge.to_node.type == "relation":
                        relation = self.text_box.find_relation(edge.to_node.name)
                        if relation == "False":
                            relation = self.text_box.create_relation(edge.to_node.name)
                            relation.object1 = table
                            relation.obj1type = edge.name
                        elif (relation.object1 == ""):
                            relation.object1 = table
                            relation.obj1type = edge.name
                        else:
                            relation.object2 = table
                            relation.obj2type = edge.name
                case "attribute":
                    if edge.to_node.type != "object":
                        relation = self.text_box.find_relation(edge.to_node.name)
                        if relation == "False":
                            relation = self.text_box.create_relation(edge.to_node.name)
                            t = "CHAR"
                            att = SQL_Attribute(edge.from_node.name,t)
                            if edge.from_node.iskey == "True":
                                relation.key.append(att)
                            relation.add_attribute(att)
                        continue
                    table = self.text_box.find_table(edge.to_node.name)
                    if table == "False":
                        table = self.text_box.create_table(edge.to_node.name)
                    t = "CHAR"
                    att = SQL_Attribute(edge.from_node.name,t)
                    if edge.to_node.iskey == "True":
                        table.key.append(att)
                    table.add_attribute(att)
                case "relation":
                    relation = self.text_box.find_relation(edge.from_node.name)
                    if relation == "False":
                        relation = self.text_box.create_relation(edge.from_node.name)
                    if edge.to_node.type != "object":
                        t = "CHAR"
                        att = SQL_Attribute(edge.to_node.name,t)
                        relation.add_attribute(att)
                        continue
                    table = self.text_box.find_table(edge.to_node.name)
                    if table == "False":
                        table = self.text_box.create_table(edge.to_node.name)
                    if relation.object1 == "":
                        relation.object1 = table
                    else:
                        relation.object2 = table
        
        for relation in self.text_box.relations:
            table1 = relation.object1
            table2 = relation.object2
            key1 = table1.key
            key2 = table2.key
            if relation.obj1type == '1':
                if relation.obj2type == '1':
                    table1.foreign_key.append(key2)
                    table1.add_attribute(key2)
                    for att in relation.attributes:
                        table1.add_attribute(att)
                else:
                    table2.foreign_key.append(key1)
                    table2.add_attribute(key1)
                    for att in relation.attributes:
                        table2.add_attribute(att)
            else:
                if relation.obj2type == '1':
                    table1.foreign_key.append(key2)
                    table1.add_attribute(key2)
                    for att in relation.attributes:
                        table1.add_attribute(att)
                else:
                    new_table = self.text_box.create_table(relation.name)
                    new_table.key.append(key1)
                    new_table.key.append(key2)
                    for att in relation.attributes:
                        new_table.add_attribute(att)
        
        for table in self.text_box.tables:
            insert_str ="CREATE TABLE "+table.name+"(\n"
            att_str = ""
            foreign_str = ""

            key_str = "    "+"PRIMARY KEY ("
            for key_att in table.key:
                if isinstance(key_att,list):
                    key_str +="("
                    for per_key in key_att:
                        key_str += per_key.name+","
                    if not key_att:
                        key_str = key_str[:-1]
                    key_str += "),"
                else:
                    key_str += key_att.name+","
            key_str +=")\n"
            
            for att in table.attributes:
                if isinstance(att,list):
                    for per_att in att:
                       att_str +="    " +per_att.name+" "+per_att.type+"("+per_att.len+"),\n"
                else:
                    att_str +="    " +att.name+" "+att.type+"("+att.len+"),\n"
            
            for foreign_key in table.foreign_key:
                foreign_str += "    "+"FOREIGN KEY ("               
                for per_key in foreign_key: 
                    foreign_str += per_key.name+","
                if not foreign_key:
                    foreign_str = foreign_str[:-1] 
                foreign_str += "),\n"
            
            self.text_box.text += insert_str+att_str+key_str+foreign_str
            self.text_box.text = self.text_box.text[:-1]+");\n"
        
        print(self.text_box.text)
        self.text_box.setPlainText(self.text_box.text)
        self.add_widgets(self.text_box)
        self.update()
        pass
    def exchange_vision(self,changeMenu,style):
        check_er = QAction('ER图',self)
        check_er.setIcon(style.standardIcon(QStyle.SP_FileIcon))
        check_er.triggered.connect(self.check_er)
        changeMenu.addAction(check_er)
        check_sql = QAction('SQL语句',self)
        style.standardIcon(QStyle.SP_FileIcon)
        check_sql.setIcon(style.standardIcon(QStyle.SP_FileIcon))
        check_sql.triggered.connect(self.check_sql)
        changeMenu.addAction(check_sql)

    def new_file(self,fileMenu,style):
        
        FileNew = QAction('新建(&N)', self)
        FileNew.setIcon(style.standardIcon(QStyle.SP_FileIcon))
        FileNew.setShortcut(Qt.CTRL + Qt.Key_N)
        FileNew.triggered.connect(self.onFileNew)
        fileMenu.addAction(FileNew)
    
    def onFileSave(self):
        pass

    def save_file(self,fileMenu,style):
        FileSave = QAction('保存(&S)', self) 
        FileSave.setIcon(style.standardIcon(QStyle.SP_DialogSaveButton)) 
        FileSave.setShortcut(Qt.CTRL + Qt.Key_S)
        FileSave.triggered.connect(self.onFileSave)  
        fileMenu.addAction(FileSave)

    def onFileSaveAs(self):
        pass
    
    def saveas_file(self,fileMenu,style):
        FileSaveAs = QAction('另存为(&A)...', self)
        FileSaveAs.setIcon(style.standardIcon(QStyle.SP_DialogSaveButton))
        FileSaveAs.triggered.connect(self.onFileSaveAs)
        fileMenu.addAction(FileSaveAs)

    def initToolBar(self):
        toolbar =  QToolBar("tool",self)
        self.addToolBar(Qt.LeftToolBarArea,toolbar)
        toolbar.setIconSize(QSize(100,50))
        #ToolBar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #ToolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        #new action
        er_object = QAction(QIcon("./images/ER_object.jpg"),"&实体",self)
        er_object.triggered.connect(self.create_object)
        er_relation = QAction(QIcon("./images/ER_relation.jpg"),"&关系",self)
        er_relation.triggered.connect(self.create_relation)
        er_attribute = QAction(QIcon("./images/ER_attribute.jpg"),"&属性",self)
        er_attribute.triggered.connect(self.create_attribute)
        
        er_link = QAction(QIcon("./images/ER_link.png"),"&连接",self)
        er_link.triggered.connect(self.create_link)

        move_area = QAction(QIcon("./images/move.jpeg"),"&挪动",self)
        move_area.triggered.connect(self.Move_Area)
        toolbar.addAction(er_object)
        toolbar.addAction(er_relation)
        toolbar.addAction(er_attribute)
        toolbar.addAction(er_link)
        toolbar.addAction(move_area)

    def Move_Area(self):
        global cursor
        pixmap = QPixmap('./images/move.jpeg')
        new_pixmap = pixmap.scaled(30,30)
        self.setCursor( QCursor(new_pixmap,15,15))
        cursor.state = "glove"

    def create_object(self):
        global cursor
        pixmap = QPixmap('./images/ER_object.jpg')
        new_pixmap = pixmap.scaled(50,30)
        self.setCursor( QCursor(new_pixmap,25,15))
        cursor.state = "object"

    def create_attribute(self):
        global cursor
        pixmap = QPixmap('./images/ER_attribute.jpg')
        new_pixmap = pixmap.scaled(30,30)
        self.setCursor( QCursor(new_pixmap,15,15))
        cursor.state = "attribute"

    def create_relation(self):
        global cursor
        pixmap = QPixmap('./images/ER_relation.jpg')
        new_pixmap = pixmap.scaled(30,30)
        temp = QCursor(new_pixmap,15,15)
        self.setCursor(temp)
        cursor.state = "relation"
    
    def create_link(self):
        global cursor
        pixmap = QPixmap('./images/ER_link.png')
        new_pixmap = pixmap.scaled(30,30)
        self.setCursor( QCursor(new_pixmap,15,15))
        cursor.state = "link"

    

class Text_Box(QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.text = ""
        self.tables = []
        self.relations = []
        self.len = 0

    def create_table(self,table_name):
        table = SQL_Table(table_name)
        self.tables.append(table)
        return table

    def create_relation(self,relation_name):
        relation = SQL_Relation(relation_name)
        self.relations.append(relation)
        return relation

    def find_table(self,table_name):
        for table in self.tables:
            print(table.name)
            if table.name == table_name:
                return table
        return "False"

    def find_relation(self,relation_name):
        for relation in self.relations:
            if relation.name == relation_name:
                return relation
        return "False"

class Coordinate_Map(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.center_layout = QVBoxLayout()
    
    def add_widget(self,widget):
        self.center_layout.addWidget(widget)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawmap(qp)
        qp.end()

    def drawmap(self, qp):
        global map_state
        global graph
        global cursor
        #set background color
        size = self.size()
        w = size.width()
        h = size.height()            
            
        qp.setPen(QColor(255, 255, 255))
        qp.setBrush(QColor(255, 255, 184))
        qp.drawRect(0, 0, w, h)
        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)
        #draw lines
        horizon_lines = int(round(h /map_state.vertical_step))
        
        vertical_lines = int(round(w/ map_state.horizon_step))


        for i in range(0,map_state.vertical_step*horizon_lines,map_state.vertical_step):
            qp.drawLine(0,i+map_state.hoffset,w,i+map_state.hoffset)
        
        for i in range(0,map_state.horizon_step*vertical_lines,map_state.horizon_step):
            qp.drawLine(i+map_state.woffset,0,i+map_state.woffset,h)

        pen = QPen(Qt.black)
        pen.setWidth(5)
        qp.setPen(pen)
        qp.setFont(QFont('SimSun', 10))
        for i in range(map_state.hoffset,map_state.vertical_step*horizon_lines,map_state.vertical_step):
            for j in range(map_state.woffset,map_state.horizon_step*vertical_lines,map_state.horizon_step):
                qp.drawPoint(j,i)
        #
        if cursor.state == "link" and cursor.press_state == "True":
            qp.drawLine(cursor.press_position[0],cursor.press_position[1],cursor.x,cursor.y)
        
        for edge in graph.edges:
            qp.drawLine(edge.from_node.x,edge.from_node.y,edge.to_node.x,edge.to_node.y)
            qp.setFont(QFont('SimSun', 25))
            rect = QRect(int((edge.from_node.x + edge.to_node.x)/2),int((edge.from_node.y + edge.to_node.y)/2),50,50)
            qp.drawText(rect,Qt.AlignCenter,edge.name)
            qp.setFont(QFont('SimSun', 10))
        #draw graph

        qp.setBrush(QColor(255, 255, 0))

        for graph_node in graph.nodes:
            #print("x={0},y={1},type={2}".format(graph_node.x,graph_node.y,graph_node.type))
            #check position visible
            if graph_node.x+map_state.origin_offset[0]<=w and graph_node.y + map_state.origin_offset[1] <=h:
                rect = QRect(graph_node.x-map_state.horizon_step+map_state.origin_offset[0],\
                            graph_node.y-map_state.vertical_step+map_state.origin_offset[1],\
                            map_state.horizon_step*2,\
                            map_state.vertical_step*2  )
                match graph_node.type:
                    case "object":
                        qp.drawRect(rect)
                        qp.drawText(rect, Qt.AlignCenter, graph_node.name)
                        
                    case "relation":
                        points = QPolygon([QPoint(graph_node.x-map_state.horizon_step+map_state.origin_offset[0],\
                                                    graph_node.y+map_state.origin_offset[1]),\
                                            QPoint(graph_node.x+map_state.origin_offset[0],\
                                                    graph_node.y+map_state.vertical_step+map_state.origin_offset[1]),\
                                            QPoint(graph_node.x+map_state.origin_offset[0]+map_state.horizon_step,\
                                                    graph_node.y+map_state.origin_offset[1]),\
                                            QPoint(graph_node.x+map_state.origin_offset[0],\
                                                    graph_node.y-map_state.vertical_step+map_state.origin_offset[1])]\
                                            )
                        qp.drawPolygon(points)
                        qp.drawText(rect, Qt.AlignCenter, graph_node.name)
                    case "attribute":
                        if graph_node.iskey == "True":
                            pen = QPen(Qt.red)
                            pen.setWidth(5)
                            qp.setPen(pen)
                        center = QPointF(graph_node.x+map_state.origin_offset[0],graph_node.y+map_state.origin_offset[1])
                        qp.drawEllipse(center, map_state.horizon_step,map_state.vertical_step)
                        qp.drawText(rect, Qt.AlignCenter, graph_node.name)
            pen =  QPen(Qt.black)
            pen.setWidth(5)
            qp.setPen(pen)

    def mouseMoveEvent(self, e):
        global cursor
        global map_state
        x = e.x()
        y = e.y()
        
        #print("x={0},y={1}".format(map_state.woffset,map_state.hoffset))
        if cursor.state == "glove":
            map_state.woffset+= x-cursor.x
            map_state.origin_offset[0]+=x-cursor.x
            map_state.woffset%=map_state.horizon_step
            map_state.hoffset+= y-cursor.y
            map_state.origin_offset[1]+=y-cursor.y
            map_state.hoffset%=map_state.vertical_step
            self.update()
        if cursor.state == "link":
            self.update()
        cursor.x = x
        cursor.y = y

    def mousePressEvent(self, event):
        global cursor
        global map_state
        global graph
        global line_edit
        cursor.press_state = "True"
        if line_edit != "":
            self.lineEdit_function()
            return
        cursor.press_position[0]=event.x()
        cursor.press_position[1]=event.y()
        cursor.x = event.x()
        cursor.y = event.y()
        if cursor.state == "default" or cursor.state == "glove" or cursor.state == "link":
            return
        real_x_pos = (cursor.x - map_state.origin_offset[0])
        mod_x_pos = real_x_pos%map_state.horizon_step
        real_y_pos = (cursor.y - map_state.origin_offset[1])
        mod_y_pos = real_y_pos%map_state.vertical_step
        
        real_x_pos -=mod_x_pos 
        real_y_pos-= mod_y_pos
        if  (mod_x_pos<= 20 and mod_y_pos <= 10):
            res = self.check_exist(real_x_pos,real_y_pos)
            if (res == "null"):
                node = Node(real_x_pos,real_y_pos,cursor.state)
                self.set_name(node,cursor.x-map_state.horizon_step,cursor.y-20)
                graph.nodes.append(node)
        elif (mod_x_pos<= 20 and mod_y_pos >= 20):
            res = self.check_exist(real_x_pos,real_y_pos+map_state.vertical_step)
            if (res == "null"):
                node = Node(real_x_pos,real_y_pos+map_state.vertical_step,cursor.state)
                self.set_name(node,cursor.x-map_state.horizon_step,cursor.y-20)
                graph.nodes.append(node)
        elif (mod_x_pos>= 45 and mod_y_pos <= 10):
            res = self.check_exist(real_x_pos+map_state.horizon_step,real_y_pos)
            if (res == "null"):
                node = Node(real_x_pos+map_state.horizon_step,real_y_pos,cursor.state)
                self.set_name(node,cursor.x-map_state.horizon_step,cursor.y-20)
                graph.nodes.append(node)
        elif (mod_x_pos>= 45 and mod_y_pos >= 20):
            res = self.check_exist(real_x_pos+map_state.horizon_step,real_y_pos+map_state.vertical_step)
            if (res == "null"):
                node = Node(real_x_pos+map_state.horizon_step,real_y_pos+map_state.vertical_step,cursor.state)
                self.set_name(node,cursor.x-map_state.horizon_step,cursor.y-20)
                graph.nodes.append(node)
        self.update()
    
    def lineEdit_function(self):
        global line_edit
        line_edit.node.name = line_edit.text()
        sip.delete(line_edit)
        line_edit = ""
        self.update()

    def set_name(self,node,x,y):
        global line_edit
        line_edit = Input_Box("", self,node)
        if cursor.state == "link":
            my_regex = QtCore.QRegExp("1|m|n")
            my_validator = QtGui.QRegExpValidator(my_regex, line_edit)
            line_edit.setValidator(my_validator)
        line_edit.returnPressed.connect(self.lineEdit_function)
        line_edit.setGeometry(x,y, map_state.horizon_step*2, 40)
        line_edit.show()

    def mouseReleaseEvent(self, event):
        global cursor
        global graph
        node1 = ""
        node2 = ""
        cursor.press_state = "False"
        self.update()
        if cursor.state != "link":
            return
        for from_node in graph.nodes:
            if (abs(cursor.press_position[0]-(from_node.x +map_state.origin_offset[0]) <= 40) and \
                abs(cursor.press_position[1] - (from_node.y+map_state.origin_offset[1]))<= 20):
                node1 = from_node
                break

        for to_node in graph.nodes:
            if(abs(cursor.x - (to_node.x +map_state.origin_offset[0])) <=40 and \
                (abs(cursor.y - (to_node.y +map_state.origin_offset[1]))<=20)):
                node2 = to_node
                break
        edge = ""
        if(node1 != "" and node2 != "" and node1 != node2):
            edge = Edge(node1,node2)
            graph.edges.append(edge)
        if(edge != "" and (node1.type == "relation" or node2.type == "relation")):
            self.set_name(edge,int((cursor.x+cursor.press_position[0])/2),int((cursor.y+cursor.press_position[1])/2))
        self.update()
        

    def check_exist(self,x,y):
        global graph
        for node in graph.nodes:
            if (abs(node.x -x) > map_state.horizon_step or abs(node.y-y)>map_state.vertical_step ):
                continue
            else:
                return "exist"
        return "null"
    def contextMenuEvent(self, event):
        global graph
        x=event.x()
        y=event.y()
        cmenu = QMenu(self)
        quitAct = cmenu.addAction("设置为主键")
        for node in graph.nodes:
            if node.type != "attribute":
                continue
            if abs(x-(node.x +map_state.origin_offset[0])) <= 40 and \
                abs(y-(node.y+map_state.origin_offset[1]))<= 20 :
                action = cmenu.exec_(self.mapToGlobal(event.pos()))
                if action == quitAct:
                    node.iskey = "True"
                    self.update()
                    return
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    screen = main_window()

        
    sys.exit(app.exec_())