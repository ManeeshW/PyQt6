import os
import sys
import numpy as np
import plotly.graph_objs as go
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication
import plotly.offline

# Create a 3D scatter plot
fig = go.Figure()
fig.add_scatter3d(
    x=np.random.rand(100),
    y=np.random.rand(100),
    z=np.random.rand(100),
    mode='markers',
    marker={'size': 30, 'color': np.random.rand(100), 'opacity': 0.6, 'colorscale': 'Viridis'}
)

# Save the plot to a temporary HTML file
temp_name = 'Temp_plot.html'
plotly.offline.plot(fig, filename=temp_name, auto_open=False)

# Create a PyQt6 application
app = QApplication(sys.argv)

# Create a web view and load the plot
web = QWebEngineView()
file_path = os.path.abspath(temp_name)
web.load(QUrl.fromLocalFile(file_path))
web.show()

# Start the application
sys.exit(app.exec())
