import os
import sys
import numpy as np
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy, QDialog, QVBoxLayout, QTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Application")
        self.images = []

        self.resize(1500, 800) # Set the default window size

        self.file_menu = self.menuBar().addMenu("&File")

        # Add "Open Folder" action
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.file_menu.addAction(self.open_folder_action)

        # Create a QLabel to display the image
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)  # Set fixed size for the image
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setScaledContents(True)

        # Create a QScrollArea to contain the QLabel
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        # Create a QSlider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)  # You can set this to the number of images
        self.slider.setValue(1)

        self.slider.valueChanged.connect(self.display_image)

        # Create a QVBoxLayout and add the QScrollArea and QSlider
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.slider)

        # Create a QWebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(800, 800) 
        self.web_view.load(QUrl("http://localhost:8050")) # Load the Dash app

        # Create a QVBoxLayout for the QScrollArea and QSlider
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.scroll_area)
        self.image_layout.addWidget(self.slider)

        # Create a QVBoxLayout for the QWebEngineView
        self.web_layout = QVBoxLayout()
        self.web_layout.addWidget(self.web_view)

        # Add the QVBoxLayouts to the main QHBoxLayout
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.image_layout)
        self.layout.addLayout(self.web_layout)

        # Create a QWidget, set its layout to QVBoxLayout
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.images = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))])
            if self.images:
                # Set the range of the QSlider
                self.slider.setRange(1, len(self.images) - 1)
                # Display the first image
                self.display_image(0)

    def display_image(self, index):
        # Load the image
        pixmap = QPixmap(self.images[index])
        # Resize the image to fit the QLabel
        pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the image to the center

# Create a PyQt6 application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
