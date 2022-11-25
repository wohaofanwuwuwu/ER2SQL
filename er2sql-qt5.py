import sys
from enum import Enum
from PyQt5 import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QFont, QColor, QPen,QPixmap,QCursor,QPolygon
from PyQt5.QtCore import QSize,QPoint,QPointF,QRect
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, 
                             QAction, QPlainTextEdit, QStyle, QFileDialog,
                             QMessageBox)
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QPushButton,QLineEdit,
    QHBoxLayout, QVBoxLayout)
from ER_Graph import Node ,Graph,Edge

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

    def onFileNew(self):
        pass
    
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
        ToolBar = self.addToolBar("tool")
        ToolBar.setIconSize(QSize(100,50))
        #ToolBar.setOrientation(Qt.Vertical)
        ToolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
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
        ToolBar.addAction(er_object)
        ToolBar.addAction(er_relation)
        ToolBar.addAction(er_attribute)
        ToolBar.addAction(er_link)
        ToolBar.addAction(move_area)

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
        
        for i in range(map_state.hoffset,map_state.vertical_step*horizon_lines,map_state.vertical_step):
            for j in range(map_state.woffset,map_state.horizon_step*vertical_lines,map_state.horizon_step):
                qp.drawPoint(j,i)
        #
        if cursor.state == "link" and cursor.press_state == "True":
            
            qp.drawLine(cursor.press_position[0],cursor.press_position[1],cursor.x,cursor.y)
        
        for edge in graph.edges:
            qp.drawLine(edge.from_node.x,edge.from_node.y,edge.to_node.x,edge.to_node.y)
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
                        center = QPointF(graph_node.x+map_state.origin_offset[0],graph_node.y+map_state.origin_offset[1])
                        qp.drawEllipse(center, map_state.horizon_step,map_state.vertical_step)
                        qp.drawText(rect, Qt.AlignCenter, graph_node.name)
        #draw edges
        
            
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
                abs(cursor.press_position[1] - (from_node.y+map_state.origin_offset[1])<= 20)):
                node1 = from_node
                break

        for to_node in graph.nodes:
            if(abs(cursor.x - (to_node.x +map_state.origin_offset[0])) <=40 and \
                (abs(cursor.y - (to_node.y +map_state.origin_offset[1]))<=20)):
                node2 = to_node
                break
        if(node1 != "" and node2 != ""):
            graph.edges.append(Edge(node1,node2))
        self.update()
        

    def check_exist(self,x,y):
        global graph
        for node in graph.nodes:
            if (abs(node.x -x) > map_state.horizon_step or abs(node.y-y)>map_state.vertical_step ):
                continue
            else:
                return "exist"
        return "null"

if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    screen = main_window()

        
    sys.exit(app.exec_())