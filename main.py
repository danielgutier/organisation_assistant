from PyQt5.QtWidgets import (QApplication,
     QMainWindow, QTabWidget)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from recorder import *
from player import *
from Parametres import *

# Only needed for access to command line arguments
import sys
        
# Subclass QMainWindow to customize the application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistant Magnetophone")
        
        self.setMinimumSize(QSize(800, 480))
        #self.showFullScreen()
        self.setMaximumSize(QSize(800, 480))
        self.showMaximized()

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabShape(QTabWidget.TabShape.Triangular)
        self.tabs.setMovable(True)
        #self.tabs.currentChanged.connect(self.onTabChange)

        self.tabs.addTab(Record(),"Enregistrer")
        self.tabs.addTab(Listen(),"Reproduire")
        self.tabs.addTab(Parametres(),"Paramètres")
        self.tabs.setFont(QFont('Helvetica',10))

        self.setCentralWidget(self.tabs)
        
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
