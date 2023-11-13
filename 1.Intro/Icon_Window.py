from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 200
        self.y = 200
        self.W = 400
        self.H = 700
        self.setGeometry(self.x,self.y,self.H,self.W)
        self.setWindowTitle("Maneesh PyQt6 GUI")
        self.setWindowIcon(QIcon("/home/maneesh/Desktop/LAB2.0/PyQt6/1.Intro/images/M.png"))
        self.setFixedHeight(400)
        self.setFixedWidth(700)
        self.setStyleSheet('background-color:green')
        self.setWindowOpacity(0.5) #0-1
 


app = QApplication(sys.argv)

window = Window()
window.show()

#sys.exit(app.exec_()) #PyQt5
sys.exit(app.exec()) #PyQt6