import os
import sys
import numpy as np
import dash
from dash import dcc, html
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget
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
    marker={'size': 30, 'color': np.random.rand(100), 'opacity': 0.6, 'colorscale': 'Viridis'}
)
fig.add_trace(scatter)

# Set the size of the figure
fig.update_layout(autosize=False, width=1000, height=1000)

# Add the scatter plot to the Dash app
graph = dcc.Graph(id='3dscatter', figure=fig)
app.layout = html.Div([
    graph,
    html.Pre(id='click-data', style={'paddingTop': 35})
])

# Update scatter plot on click
@app.callback(
    dd.Output('click-data', 'children'),
    dd.Input('3dscatter', 'clickData'))

def display_click_data(clickData):
    print(clickData)
    return f'You clicked on point: {clickData}'

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

# Create a QLabel to display the image
label = QLabel()
pixmap = QPixmap('/home/maneesh/Desktop/LAB2.0/dash/43/0045.jpg')
label.setPixmap(pixmap)

# Create a QWebEngineView and load the Dash app
web = QWebEngineView()
web.load(QUrl("http://localhost:8050"))
web.setFixedSize(1000, 1000)

# Add the QLabel and QWebEngineView to the layout
layout.addWidget(label)
layout.addWidget(web)
widget.setLayout(layout)
widget.show()

# Start the PyQt6 application
sys.exit(qt_app.exec())
