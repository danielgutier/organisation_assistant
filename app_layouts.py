from PyQt5.QtWidgets import (
    QPushButton, QLineEdit,
    QWidget, QLabel, QVBoxLayout,
    QDialog, QComboBox, QDialogButtonBox    
    )
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
import os, datetime

# Only needed for access to command line arguments


soundspath=os.path.join(os.getcwd(),"sounds")
users=os.listdir(soundspath)
for elem in users :
    if not os.path.isdir(os.path.join(soundspath,elem)):
        users.remove(elem)

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)
        
class Record(QWidget):
    def __init__(self):
        super().__init__()

        fontbig=QFont('Helvetica',15)
        fontsmall=QFont('Helvetica',10)
        # Menu déroulant voix
        self.menuderoulant=QComboBox()
        self.menuderoulant.addItems(["Père","Mère","Enseignant"])
        self.menuderoulant.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menuderoulant.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menuderoulant.currentTextChanged.connect( self.text_changed )
        
        # Button REC
        self.button_rec=QPushButton("Enregistrer")
        #self.button_rec.setIconSize(QSize(40,40))
        #self.button_rec.setIcon(QIcon("images/pause_up.png"))
        self.button_rec.setFont(fontbig)
        self.button_rec.button_is_checked = False
        self.button_rec.setCheckable(True)
        self.button_rec.clicked.connect(self.rec_was_toggled)

        
        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        # status.setText(personne)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menuderoulant)
        self.layout.addWidget(self.button_rec)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
        
    def rec_was_toggled(self, checked):
        self.button_is_checked = checked
        if checked:
            self.button_rec.setText("Arreter")
            self.status.setText("Enregistrement")
        else:
            self.button_rec.setText("Enregistrer")
            self.status.setText("Prêt")
            
        print("Checked ?",self.button_is_checked)
                
    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)

class Listen(QWidget):
    def __init__(self):
        super().__init__()

        fontbig=QFont('Helvetica',15)
        fontsmall=QFont('Helvetica',10)
        
        # Menu déroulant utilisateurs
        self.menu_user=QComboBox()
        self.menu_user.addItems(users)
        self.menu_user.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menu_user.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menu_user.currentTextChanged.connect( self.text_changed )
        
        # Menu déroulant fichiers
        self.menu_fichiers=QComboBox()
        filelist=os.listdir(os.path.join(soundspath,users[0]))
        sound_items=[]
        for filen in filelist:
            if (not filen.endswith(".wav")) and (not  filen.endswith(".flac")) :
                filelist.remove(filen)
            else:
                sound_items.append(datetime.datetime(int(filen[0:4]),int(filen[4:6]),int(filen[6:8]),int(filen[9:11]),int(filen[11:13]),int(filen[13:15])).strftime("%H:%M:%S %A %d-%m-%Y"))
        self.menu_fichiers.addItems(sound_items)
        self.menu_fichiers.setFont(fontsmall)
        # Sends the current index (position) of the selected item.
        self.menu_fichiers.currentIndexChanged.connect( self.file_ind_changed )
        # There is an alternate signal to send the text.
        self.menu_fichiers.currentTextChanged.connect( self.file_changed )
        
        # Button REC
        self.button_rec=QPushButton("Écouter")
        self.button_rec.setFont(fontbig)
        self.button_rec.button_is_checked = False
        self.button_rec.setCheckable(True)
        self.button_rec.clicked.connect(self.rec_was_toggled)
        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        # status.setText(personne)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menu_user)
        self.layout.addWidget(self.menu_fichiers)
        self.layout.addWidget(self.button_rec)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
        
    def rec_was_toggled(self, checked):
        self.button_is_checked = checked
        if checked:
            self.button_rec.setText("Arreter")
            self.status.setText("Écoute")
        else:
            self.button_rec.setText("Écouter")
            self.status.setText("Prêt")
            
        print("Checked ?",self.button_is_checked)
                
    def index_changed(self, i): # i is an int
        self.menu_fichiers.clear()
        print("index",i)
        filelist=os.listdir(os.path.join(soundspath,users[i]))
        sound_items=[]
        for filen in filelist:
            if (not filen.endswith(".wav")) and (not  filen.endswith(".flac")) :
                filelist.remove(filen)
            else:
                sound_items.append(datetime.datetime(int(filen[0:4]),int(filen[4:6]),int(filen[6:8]),int(filen[9:11]),int(filen[11:13]),int(filen[13:15])).strftime("%H:%M:%S %A %d-%m-%Y"))
        self.menu_fichiers.addItems(sound_items)

    def text_changed(self, s): # s is a str
        print(s)
        
    def file_ind_changed(self, i): # i is an int
        print("index",i)

    def file_changed(self, s): # s is a str
        print(s)
        
class Users(QWidget):
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