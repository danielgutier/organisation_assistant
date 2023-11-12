# Import modules for GUI handling
from PyQt5.QtWidgets import (
    QPushButton, QWidget, QLabel, 
    QVBoxLayout, QComboBox,
    QApplication
    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import file, date, language and database functions  
import os, datetime, locale, db_manip
# Linux based system
locale.setlocale(locale.LC_TIME,'fr_CH.utf8')
# Windows based system
# locale.setlocale(locale.LC_TIME,'fr_FR')

# Import sound playing modules
import sounddevice as sd
from playsound import playsound

# Import text to speech modules
import pyttsx3 # offline
from gtts import gTTS # online

# Internet connection test
import socket
def check_internet_connection():
    remote_server = "www.google.com"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((remote_server, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()

# Some global variables
soundspath=os.path.join(os.getcwd(),"sounds")
textspath=os.path.join(os.getcwd(),"texts")

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)

# Main player tab Dialog class
class Listen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Combobox Users
        self.menu_user=QComboBox()
        self.menu_user.addItems(db_manip.get_users())
        self.menu_user.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menu_user.currentIndexChanged.connect( self.index_changed )
        
        # Audio files Label
        self.text_audiofiles=QLabel("Fichiers Audio")
        self.text_audiofiles.setScaledContents(True)
        self.text_audiofiles.setFont(fontmedium)
        
        # Combobox audio files
        self.menu_fichiers_audio=QComboBox()
        current_user=db_manip.get_audiodates(self.menu_user.currentText())
        sound_items=[]
        for filen in current_user:
            sound_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers_audio.addItems(sound_items)
        self.menu_fichiers_audio.setFont(fontsmall)
        
        # Button play audio
        self.button_play_audio=QPushButton("Écouter Audio")
        self.button_play_audio.setFont(fontbig)
        self.button_play_audio.setEnabled(True)
        self.button_play_audio.clicked.connect(self.play_was_toggled_audio)
        
        # Text files Label
        self.text_textfiles=QLabel("Fichiers Texte")
        self.text_textfiles.setScaledContents(True)
        self.text_textfiles.setFont(fontmedium)
        
        # Combobox text files
        self.menu_fichiers_text=QComboBox()
        current_user=db_manip.get_textdates(self.menu_user.currentText())
        text_items=[]
        for filen in current_user:
            text_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers_text.addItems(text_items)
        self.menu_fichiers_text.setFont(fontsmall)
        
        # Button play text
        self.button_play_text=QPushButton("Écouter Texte")
        self.button_play_text.setFont(fontbig)
        self.button_play_text.setEnabled(True)
        self.button_play_text.clicked.connect(self.play_was_toggled_text)
        
        # Button Rafraichir
        self.button_refresh=QPushButton("Rafraichir")
        self.button_refresh.setFont(fontbig)
        self.button_refresh.setEnabled(True)
        self.button_refresh.clicked.connect(self.refresh_was_toggled)
        
        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menu_user)
        self.layout.addWidget(self.text_audiofiles)
        self.layout.addWidget(self.menu_fichiers_audio)
        self.layout.addWidget(self.button_play_audio)
        self.layout.addWidget(self.text_textfiles)
        self.layout.addWidget(self.menu_fichiers_text)
        self.layout.addWidget(self.button_play_text)
        self.layout.addStretch()
        self.layout.addWidget(self.button_refresh)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
        
    def play_was_toggled_audio(self):
        if self.menu_fichiers_audio.currentText() :
            QApplication.processEvents()
            self.button_play_audio.setEnabled(False)
            self.button_play_text.setEnabled(False)
            self.status.setText("Écoute")

            sound_fname=os.path.join(soundspath,self.menu_user.currentText(),db_manip.get_audiofile_name(self.menu_fichiers_audio.currentText()))
            print(sound_fname)
            playsound(sound_fname)
        else:
            print ("No file")
            
        self.button_play_audio.setEnabled(True)
        self.button_play_text.setEnabled(True)
        self.status.setText("Prêt")
        
    def play_was_toggled_text(self):
        if self.menu_fichiers_text.currentText():
            self.button_play_audio.setEnabled(False)
            self.button_play_text.setEnabled(False)
            self.status.setText("Écoute")

            text_fname=os.path.join(textspath,self.menu_user.currentText(),db_manip.get_textfile_name(self.menu_fichiers_text.currentText()))
            with open (text_fname,'r') as f:   
                mytext = f.readlines()
            f.close()
            print(mytext[0])
            
            if check_internet_connection():
                print ("Online")
                myobj = gTTS(text=mytext[0], lang='fr', slow=False)
                # Saving the converted audio 
                myobj.save("temp.mp3")
                # Playing the converted file
                playsound('temp.mp3')

            else:
                print("Offline")
                engine = pyttsx3.init()
                engine.setProperty('voice', "french")
                engine.setProperty('rate',130)
                engine.say(mytext[0])
                engine.runAndWait()
        else:
            print ("No file")
            
        self.button_play_audio.setEnabled(True)
        self.button_play_text.setEnabled(True)
        self.status.setText("Prêt")
        
    def index_changed(self, i): # i is an int
        print("index",i)
        self.menu_fichiers_audio.clear()
        current_user=db_manip.get_audiodates(self.menu_user.currentText())
        sound_items=[]
        for filen in current_user:
            sound_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers_audio.addItems(sound_items)
        
        self.menu_fichiers_text.clear()
        current_user=db_manip.get_textdates(self.menu_user.currentText())
        text_items=[]
        for filen in current_user:
            text_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers_text.addItems(text_items)

    def refresh_was_toggled(self):
        self.menu_user.clear()
        users_items=db_manip.get_users()
        self.menu_user.addItems(users_items)
        self.index_changed(self)
