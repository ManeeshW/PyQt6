import os
import sys
import numpy as np
from PyQt6.QtGui import QPixmap, QAction, QPalette, QTransform, QPainter
from PyQt6.QtCore import QUrl, Qt, QSize, QRectF, QSizeF
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy, QDialog, QVBoxLayout, QTextEdit, QGraphicsScene, QGraphicsView
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

        # Create a QGraphicsView to display the image
        self.image_view = QGraphicsView()
        self.image_view.setFixedSize(640, 480)  # Set fixed size for the image
        self.image_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.image_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.image_view.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True)
        self.image_view.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontSavePainterState, True)
        self.image_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.image_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.image_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # Initialize the zoom level
        self.zoom_level = 0

        # Add a QScrollArea to enable scrolling
        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area.setWidget(self.image_view)
        self.scroll_area.setVisible(True)

        # Create a QSlider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)  # You can set this to the number of images
        self.slider.setValue(1)
        self.slider.valueChanged.connect(self.display_image)

        # Create a QWebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(800, 800) 
        self.web_view.load(QUrl("http://localhost:8050")) 

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

    def wheelEvent(self, event):
        zoomInFactor = 1.15
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.image_view.mapToScene(event.position().toPoint())

        # Zoom
        if event.angleDelta().y() > 0:
            if self.zoom_level < 100:  # Increase the zoom in level limit
                self.zoom_level += 1
                self.image_view.setTransform(self.image_view.transform().scale(zoomInFactor, zoomInFactor))
        else:
            if self.zoom_level > 0:  # Limit the zoom out level
                self.zoom_level -= 1
                self.image_view.setTransform(self.image_view.transform().scale(zoomOutFactor, zoomOutFactor))

        # Reset the scroll bars
        self.scroll_area.horizontalScrollBar().setValue(0)
        self.scroll_area.verticalScrollBar().setValue(0)


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
        # Create a QGraphicsScene and add the pixmap to it
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.image_view.setScene(scene)

    

# Create a PyQt6 application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
