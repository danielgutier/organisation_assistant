from PyQt5.QtWidgets import (
    QPushButton, QWidget, QLabel, 
    QVBoxLayout, QComboBox
    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os, datetime
import sounddevice as sd
import soundfile as sf
import db_manip
import locale
locale.setlocale(locale.LC_TIME,'fr_FR')

# Only needed for access to command line arguments


""" soundspath=os.path.join(os.getcwd(),"sounds")
users=os.listdir(soundspath)
for elem in users :
    if not os.path.isdir(os.path.join(soundspath,elem)):
        users.remove(elem)
        
def filen(user_index,file_index):
    filelist=os.listdir(os.path.join(soundspath,users[user_index]))
    return os.path.join(soundspath,users[user_index],filelist[file_index])"""

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)




class Listen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Menu déroulant utilisateurs
        self.menu_user=QComboBox()
        self.menu_user.addItems(db_manip.get_users(True))
        self.menu_user.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menu_user.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menu_user.currentTextChanged.connect( self.text_changed )
        
        # Menu déroulant fichiers
        self.menu_fichiers=QComboBox()
        #print(self.menu_user.currentText)
        current_user=db_manip.get_audiodates(self.menu_user.currentText())
        sound_items=[]
        for filen in current_user:
            sound_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%H:%M:%S %A %d-%m-%Y"))
        self.menu_fichiers.addItems(sound_items)
        self.menu_fichiers.setFont(fontsmall)
        # Sends the current index (position) of the selected item.
        self.menu_fichiers.currentIndexChanged.connect( self.file_ind_changed )
        # There is an alternate signal to send the text.
        self.menu_fichiers.currentTextChanged.connect( self.file_changed )
        
        # Button play
        self.button_play=QPushButton("Écouter")
        self.button_play.setFont(fontbig)
        #self.button_play.button_is_checked = False
        self.button_play.setEnabled(True)
        self.button_play.clicked.connect(self.play_was_toggled)
        
        # Button stop
        self.button_stop=QPushButton("Arreter")
        self.button_stop.setFont(fontbig)
        #self.button_stop.button_is_checked = False
        self.button_stop.setEnabled(False)
        self.button_stop.clicked.connect(self.stop_was_toggled)
        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        # status.setText(personne)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menu_user)
        self.layout.addWidget(self.menu_fichiers)
        self.layout.addWidget(self.button_play)
        self.layout.addWidget(self.button_stop)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
        
    def play_was_toggled(self):
        self.button_play.setEnabled(False)
        self.status.setText("Écoute")
        self.button_stop.setEnabled(True)
        sound_fname=filen(self.menu_user.currentIndex(),self.menu_fichiers.currentIndex())
        data, fs = sf.read(sound_fname)
        sd.play(data, fs)
        sd.wait()

    def stop_was_toggled(self):
        self.button_stop.setEnabled(False)
        self.status.setText("Prêt")
        self.button_play.setEnabled(True)
            
                
    def index_changed(self, i): # i is an int
        self.menu_fichiers.clear()
        print("index",i)
        # filelist=os.listdir(os.path.join(soundspath,users[i]))
        # sound_items=[]
        # for filen in filelist:
        #     if (not filen.endswith(".wav")) and (not  filen.endswith(".flac")) :
        #         filelist.remove(filen)
        #     else:
        #         sound_items.append(datetime.datetime(int(filen[0:4]),int(filen[4:6]),int(filen[6:8]),int(filen[9:11]),int(filen[11:13]),int(filen[13:15])).strftime("%H:%M:%S %A %d-%m-%Y"))
        current_user=db_manip.get_audiodates(self.menu_user.currentText())
        sound_items=[]
        for filen in current_user:
            sound_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%H:%M:%S %A %d-%m-%Y"))
        self.menu_fichiers.addItems(sound_items)

    def text_changed(self, s): # s is a str
        print(s)
        
    def file_ind_changed(self, i): # i is an int
        print("index",i)

    def file_changed(self, s): # s is a str
        print(s)
        print(self.menu_fichiers.currentText())