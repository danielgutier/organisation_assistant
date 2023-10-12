from PyQt5.QtWidgets import (QApplication,
     QMainWindow, QTabWidget)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from recorder import *
from player import *
from Parametres import *

# Only needed for access to command line arguments
import sys

from keyboard import press

        
# Subclass QMainWindow to customize the application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistant Magnetophone")
        
        self.setMinimumSize(QSize(800, 480))
        #self.showFullScreen()
        self.setMaximumSize(QSize(800, 480))
        self.showMaximized()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setTabShape(QTabWidget.TabShape.Triangular)
        tabs.setMovable(True)

        tabs.addTab(Record(),"Enregistrer")
        tabs.addTab(Listen(),"Reproduire")
        tabs.addTab(Parametres(),"Paramètres")
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
sys.exit(app.exec())


# Your application won't reach here until you exit and the event
# loop has stopped.
