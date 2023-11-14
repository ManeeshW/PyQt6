import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        self.plot()
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        #ax = fig.add_subplot(111, projection = '3d')
        # create an axis
        #ax = self.figure.add_subplot(111) #2d
        ax = self.figure.add_subplot(111, projection = '3d')
        x = [0, 2, 0,0]
        y = [0, 2, 0,2]
        z = [0, 2, 2,0]

        scatter = ax.scatter(x,y,z,picker=True)

        # # discards the old graph
        # ax.clear()

        # # plot data
        # ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
        self.canvas.mpl_connect('pick_event', lambda event: self.chaos_onclick(event, ax, x, y, z))

    def chaos_onclick(self, event, ax, x, y, z):

        point_index = int(event.ind)
        print(point_index)

        #proj = ax.get_proj()
        #x_p, y_p, _ = proj3d.proj_transform(x[point_index], y[point_index], z[point_index], proj)
        #plt.annotate(str(point_index), xy=(x_p, y_p))
        
        print("X=",x[point_index], " Y=",y[point_index], " Z=",z[point_index], " PointIdx=", point_index)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec())