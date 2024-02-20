import os
import sys
import numpy as np
import dash
from dash import dcc, html
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objs import Scatter3d, Figure
import dash.dependencies as dd

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Your Application")

        # Create the File menu
        self.menu = self.menuBar().addMenu("&File")

        # Add "Open Folder" action
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.menu.addAction(self.open_folder_action)

        # Add "Save" action
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save)
        self.menu.addAction(self.save_action)

        # Add "Save As" action
        self.save_as_action = QAction("Save As", self)
        self.save_as_action.triggered.connect(self.save_as)
        self.menu.addAction(self.save_as_action)

        # Create the Help menu
        self.help_menu = self.menuBar().addMenu("&Help")

        # Add "About" action
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addAction(self.about_action)

        # Add other menus here...

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            print(f"Folder selected: {folder_path}")

    def save(self):
        print("Save clicked")

    def save_as(self):
        print("Save As clicked")

    def about(self):
        print("About clicked")
        print("This is an open-source application developed by Maneesha Wickramasuriya.")

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

# Run the Dash app in a separate thread
from threading import Thread
def run_dash():
    app.run_server(port=8050)

Thread(target=run_dash).start()

# Create a PyQt6 application
qt_app = QApplication(sys.argv)

# Create a QWidget to hold the QLabel and QWebEngineView
widget = QWidget()
layout = QHBoxLayout()  

# Create a QVBoxLayout for the QLabel and QSlider
image_layout = QVBoxLayout()

# Create a QLabel to display the image
label = QLabel()

# Create a QSlider
slider = QSlider(Qt.Orientation.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)  # You can set this to the number of images
slider.setValue(1)

# Function to update image based on slider value
def update_image(value):
    # Assuming images are named as 'image0.jpg', 'image1.jpg', etc.
    # and are all in the same directory
    image_path = '/home/maneesh/Desktop/LAB2.0/dash/43/{:04d}.jpg'.format(value)
    pixmap = QPixmap(image_path)
    label.setPixmap(pixmap)
    slider.setFixedWidth(label.width())  # Set the slider width to the image width

# Connect the slider's value changed signal to the update image function
slider.valueChanged.connect(update_image)

# Create buttons
next_button = QPushButton("NEXT")
back_button = QPushButton("BACK")
calculate_button = QPushButton("CALCULATE")
reset_button = QPushButton("RESET")

# Function to handle button clicks
def handle_button_click(button):
    if button == next_button:
        slider.setValue(slider.value() + 1)
    elif button == back_button:
        slider.setValue(slider.value() - 1)
    elif button in [calculate_button, reset_button]:
        print(f'Button "{button.text()}" clicked. Current image: {slider.value()}')

# Connect button clicks to the handler
back_button.clicked.connect(lambda: handle_button_click(back_button))
next_button.clicked.connect(lambda: handle_button_click(next_button))
calculate_button.clicked.connect(lambda: handle_button_click(calculate_button))
reset_button.clicked.connect(lambda: handle_button_click(reset_button))

# Create a QHBoxLayout for the buttons
button_layout = QHBoxLayout()
button_layout.addWidget(back_button)
button_layout.addWidget(next_button)
button_layout.addWidget(calculate_button)
button_layout.addWidget(reset_button)

# Add the QLabel, QSlider, and buttons to the image_layout
image_layout.addLayout(button_layout)
image_layout.addWidget(label)
image_layout.addWidget(slider)

# Create a QWebEngineView and load the Dash app
web = QWebEngineView()
web.load(QUrl("http://localhost:8050"))
web.setFixedSize(800, 800)  # Adjust the size to fit the window

# Add the QVBoxLayout to the QHBoxLayout
layout.addLayout(image_layout)
layout.addWidget(web)

# Set the layout of the QWidget
widget.resize(2000, 1000) # Set the default window size
widget.setLayout(layout)

# Create a QMainWindow
window = MainWindow()

# Show the QMainWindow
widget.show()
window.show()

# Run the QApplication
qt_app.exec()
