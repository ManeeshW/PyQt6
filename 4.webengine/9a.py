import os
import sys
import numpy as np
import dash
from dash import dcc, html
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSlider, QHBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objs import Scatter3d, Figure
import dash.dependencies as dd

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
next_button.clicked.connect(lambda: handle_button_click(next_button))
back_button.clicked.connect(lambda: handle_button_click(back_button))
calculate_button.clicked.connect(lambda: handle_button_click(calculate_button))
reset_button.clicked.connect(lambda: handle_button_click(reset_button))

# Add the QLabel and QSlider to the image_layout
image_layout.addWidget(next_button)
image_layout.addWidget(back_button)
image_layout.addWidget(calculate_button)
image_layout.addWidget(reset_button)
image_layout.addWidget(label)
image_layout.addWidget(slider)

# Create a QWebEngineView and load the Dash app
web = QWebEngineView()
web.load(QUrl("http://localhost:8050"))
web.setFixedSize(800, 800)  # Adjust the size to fit the window

# Add the image_layout and QWebEngineView to the layout
layout.addLayout(image_layout)
layout.addWidget(web)
widget.setLayout(layout)
widget.show()

# Start the PyQt6 application
sys.exit(qt_app.exec())
