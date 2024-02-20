import os
import sys
import numpy as np
import dash
from dash import dcc, html
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSlider, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objs import Scatter3d, Figure
import dash.dependencies as dd


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.image = None

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        # Save the scene pos
        old_pos = self.mapToScene(event.position().toPoint())

        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

        # Get the new position
        new_pos = self.mapToScene(event.position().toPoint())

        # Move scene to old position
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            pos = event.position()
            self.draw_dot(pos.x(), pos.y())
            print(f"Pixel coordinates: ({pos.x()}, {pos.y()})")

    def draw_dot(self, x, y):
        if self.image is not None:
            painter = QPainter(self.image)
            pen = QPen(Qt.GlobalColor.green)
            pen.setWidth(10)
            painter.setPen(pen)
            painter.drawPoint(x, y)
            painter.end()
            self.update()

    def set_image(self, image):
        self.image = image



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
layout = QHBoxLayout()  # Change QVBoxLayout to QHBoxLayout

# Create a QVBoxLayout for the QLabel and QSlider
image_layout = QVBoxLayout()

# Create a GraphicsView and QGraphicsScene
view = GraphicsView()
scene = QGraphicsScene()
view.setScene(scene)

# Create a QGraphicsPixmapItem and add it to the scene
pixmap_item = QGraphicsPixmapItem()
scene.addItem(pixmap_item)

# Function to update image based on slider value
def update_image(value):
    # Assuming images are named as 'image0.jpg', 'image1.jpg', etc.
    # and are all in the same directory
    image_path = '/home/maneesh/Desktop/LAB2.0/dash/43/{:04d}.jpg'.format(value)
    pixmap = QPixmap(image_path)
    pixmap_item.setPixmap(pixmap)

# Create a QSlider
slider = QSlider(Qt.Orientation.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)  # You can set this to the number of images
slider.setValue(1)

# Connect the slider's value changed signal to the update image function
slider.valueChanged.connect(update_image)

# Add the QGraphicsView and QSlider to the image_layout
image_layout.addWidget(view)
image_layout.addWidget(slider)

# Create a QWebEngineView and load the Dash app
web = QWebEngineView()
web.load(QUrl("http://localhost:8050"))
web.setFixedSize(800, 800)  # Adjust the size to fit the window

# Add the image_layout and QWebEngineView to the layout
layout.addLayout(image_layout)
layout.addWidget(web)
# Set the default window size
widget.resize(2000, 1000)
widget.setLayout(layout)
widget.show()

# Start the PyQt6 application
sys.exit(qt_app.exec())
