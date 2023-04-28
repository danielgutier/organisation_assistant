from PyQt5.QtWidgets import (QApplication,
     QMainWindow, QTabWidget)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont

from app_layouts import *

# Only needed for access to command line arguments
import sys

# Needed to control sound functions
from sound_functions import *
from keyboard import press
from create_fname import *
# Subclass Qwidget to customize each widget


        
# Subclass QMainWindow to customize the application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistant Magnetophone")
        
        self.setMinimumSize(QSize(400, 240))
        self.showMaximized()
        #self.showFullScreen()
        #self.setMaximumSize(QSize(800, 480))

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setTabShape(QTabWidget.TabShape.Triangular)
        tabs.setMovable(True)

        tabs.addTab(Record(),"Enregistrer")
        tabs.addTab(Listen(),"Reproduire")
        tabs.addTab(Users(),"Utilisateurs")
        tabs.setFont(QFont('Helvetica',10))

        self.setCentralWidget(tabs)
        
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
#window = QWidget()

# Create à main window
window=MainWindow()

# Next command will open a window with a button
#window = QPushButton("Push Me")
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
