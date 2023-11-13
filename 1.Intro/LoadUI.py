import typing
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6 import QtCore, uic

class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("/home/maneesh/Desktop/LAB2.0/PyQt6/1.Intro/WindowUI.ui",self)

app = QApplication(sys.argv)

window = UI()

window.show()

app.exec() #PyQt6