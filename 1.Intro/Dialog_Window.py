from PyQt6.QtWidgets import QApplication, QDialog
import sys

app = QApplication(sys.argv)

window = QDialog()

window.show()

#sys.exit(app.exec_()) #PyQt5
sys.exit(app.exec()) #PyQt6
