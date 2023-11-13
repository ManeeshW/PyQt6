from PyQt6.QtWidgets import QApplication, QWidget
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


app = QApplication(sys.argv)

window = Window()
window.show()

#sys.exit(app.exec_()) #PyQt5
sys.exit(app.exec()) #PyQt6