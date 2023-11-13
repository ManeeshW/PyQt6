from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)

window = QMainWindow()
window.statusBar().showMessage("Welcome to PyQt6")
#window.menuBar().addMenu("File")
window.menuBar().addMenu("File").addMenu("edit")
window.show()

#sys.exit(app.exec_()) #PyQt5
sys.exit(app.exec()) #PyQt6

