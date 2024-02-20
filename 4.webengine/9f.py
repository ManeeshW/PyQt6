import os
import sys
import numpy as np
import dash
from dash import dcc, html
import dash.dependencies as dd
from plotly.graph_objs import Scatter3d, Figure
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy, QDialog, QVBoxLayout, QTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Create a Dash app
app = dash.Dash(__name__)

# Create a 3D scatter plot
fig = Figure()
scatter = Scatter3d(
    x=np.random.rand(100),
    y=np.random.rand(100),
    z=np.random.rand(100),
    mode='markers',
    marker={'size': 3, 'color': ['blue']*100, 'opacity': 0.6,}
)
fig.add_trace(scatter)

# Set the size of the figure
fig.update_layout(autosize=False, width=800, height=800)  # Adjust the size to fit the window

# Add the scatter plot to the Dash app
graph = dcc.Graph(id='3dscatter', figure=fig)
app.layout = html.Div([
    graph,
    html.Pre(id='click-data', style={'paddingTop': 35})
])

# Update scatter plot on click
@app.callback(
    dd.Output('3dscatter', 'figure'),
    dd.Output('click-data', 'children'),
    dd.Input('3dscatter', 'clickData'),
    dd.State('3dscatter', 'figure'))

def update_color(clickData, figure):
    if clickData:
        point = clickData['points'][0]
        if 'pointIndex' in point:
            for i in figure['data']:
                if i['type'] == 'scatter3d':
                    colors = i['marker']['color']
                    colors[point['pointIndex']] = 'red'
                    i['marker']['color'] = colors
            return figure, f'You clicked on point: {clickData}'
    return dash.no_update, dash.no_update


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText("This is an open-source application developed by Maneesha Wickramasuriya.")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Your Application")

        # Initialize images attribute
        self.images = []

        # Set the default window size
        self.resize(1500, 700)

        # Create the File menu
        self.file_menu = self.menuBar().addMenu("&File")

        # Add "Open Folder" action
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.file_menu.addAction(self.open_folder_action)

        # Add "Save" action
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save)
        self.file_menu.addAction(self.save_action)

        # Add "Save As" action
        self.save_as_action = QAction("Save As", self)
        self.save_as_action.triggered.connect(self.save_as)
        self.file_menu.addAction(self.save_as_action)

        # Add "Exit" action
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.exit_application)
        self.file_menu.addAction(self.exit_action)

        # Create the Help menu
        self.help_menu = self.menuBar().addMenu("&Help")

        # Add "About" action
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addAction(self.about_action)

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
        self.slider.valueChanged.connect(self.change_image)

        # Create a QVBoxLayout and add the QScrollArea and QSlider
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.slider)

        # Create a QWebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(800, 800) 

        # Load the Dash app
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

        # # Create a QVBoxLayout and add the QWebEngineView
        # self.layout = QHBoxLayout()
        # self.layout.addWidget(self.scroll_area)
        # self.layout.addWidget(self.web_view)

        # Create a QWidget, set its layout to QVBoxLayout
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            # Get a list of the .jpg and .png files in the folder
            self.images = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))])
            if self.images:
                # Set the range of the QSlider
                self.slider.setRange(0, len(self.images) - 1)
                # Display the first image
                self.display_image(0)

    def display_image(self, index):
        # Load the image
        pixmap = QPixmap(self.images[index])
        # Resize the image to fit the QLabel
        pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        # Set the QPixmap to the QLabel
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the image to the center

    def change_image(self, value):
        self.display_image(value)

    def save(self):
        print("Save clicked")

    def save_as(self):
        print("Save As clicked")

    def about(self):
        self.dialog = AboutDialog()
        self.dialog.exec()

    def exit_application(self):
        os._exit(0)

    def closeEvent(self, event):
        os._exit(0)

# Run the Dash app in a separate thread
from threading import Thread
def run_dash():
    app.run_server(port=8050)

Thread(target=run_dash).start()

# Create a PyQt6 application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
