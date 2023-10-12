from PyQt5.QtWidgets import (
    QPushButton, QLineEdit,
    QWidget, QLabel, QVBoxLayout,
    QDialog, QComboBox, QDialogButtonBox    
    )
from PyQt5.QtCore import (QSize, Qt, 
    QObject, QThread, pyqtSignal)
from PyQt5.QtGui import QFont
import os, datetime, sound_functions, keyboard

# Only needed for access to command line arguments


soundspath=os.path.join(os.getcwd(),"sounds")
users=os.listdir(soundspath)
for elem in users :
    if not os.path.isdir(os.path.join(soundspath,elem)):
        users.remove(elem)

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)
       
class Parametres(QWidget):
    def __init__(self):
        super().__init__()

        # Menu déroulant voix
        self.menuderoulant=QComboBox()
        self.menuderoulant.addItems(["Père","Mère","Enseignant"])
        self.menuderoulant.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menuderoulant.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menuderoulant.currentTextChanged.connect( self.text_changed )
        
        # Button REC
        self.button_add=QPushButton("Ajouter utilisateur")
        self.button_add.setFont(fontbig)
        #self.button_add.button_is_checked = False
        #self.button_add.setCheckable(True)
        self.button_add.clicked.connect(self.add_was_clicked)

        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        # status.setText(personne)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menuderoulant)
        self.layout.addWidget(self.button_add)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
        
    def add_was_clicked(self, s):
        print("Checked ?",s)
        
        dlg = Add_User()
         
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
            self.menuderoulant.addItem(users[-1])
        else:
            print("Cancel!")
                
    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)
        
class Add_User(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter utilisateur")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Nom de l'utilisateur")
        message.setAlignment(Qt.AlignmentFlag.AlignTop)
        message.setScaledContents(True)
        message.setFont(fontmedium)
        self.newuser=QLineEdit()
        self.layout.addWidget(message)
        self.layout.addWidget(self.newuser)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    def accept(self) -> None:
        users.append(self.newuser.text())
        return super().accept()