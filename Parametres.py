from PyQt5.QtWidgets import (
    QPushButton, QLineEdit,
    QWidget, QLabel, QVBoxLayout,
    QDialog, QComboBox, QDialogButtonBox,
    QDateEdit
    )
from PyQt5.QtCore import (
    QSize, Qt, QDateTime
    )
from PyQt5.QtGui import (
    QFont, QPalette, 
    QColor
    )
import soundfile as sf
import os, datetime, db_manip, locale
locale.setlocale(locale.LC_TIME,'fr_FR')

# Function to test internet connection
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

# Some global (Parametres tab) variables
soundspath=os.path.join(os.getcwd(),"sounds")
textspath=os.path.join(os.getcwd(),"texts")

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)
       
class Parametres(QWidget):
    def __init__(self):
        super().__init__()
        
        # Button Add User
        self.button_add_user=QPushButton("Ajouter utilisateur")
        self.button_add_user.setFont(fontbig)
        self.button_add_user.clicked.connect(self.add_was_clicked)
        
        # Button Remove User        
        self.button_remove_user=QPushButton("Enlever utilisateur")
        self.button_remove_user.setFont(fontbig)
        self.button_remove_user.clicked.connect(self.remove_was_clicked)
        
        # Delete files label
        self.text_delete_files=QLabel("Effacer des fichiers")
        self.text_delete_files.setScaledContents(True)
        self.text_delete_files.setFont(fontmedium)
        
        # Button Delete Audio
        self.button_delete_audio=QPushButton("Effacer un fichier audio")
        self.button_delete_audio.setFont(fontbig)
        self.button_delete_audio.clicked.connect(self.button_delete_audio_was_toggled)
        # Button Delete text
        self.button_delete_text=QPushButton("Effacer un fichier texte")
        self.button_delete_text.setFont(fontbig)
        self.button_delete_text.clicked.connect(self.button_delete_text_was_toggled)
        
        # Convert label
        self.text_convert_audiofiles=QLabel("Convertir des fichiers audio")
        self.text_convert_audiofiles.setScaledContents(True)
        self.text_convert_audiofiles.setFont(fontmedium)
        
        # Button Convert from Date
        self.button_convert=QPushButton("Convertir un fichier audio")
        self.button_convert.setFont(fontbig)
        self.button_convert.clicked.connect(self.convert_was_toggled)
        
        # Button Convert from Date
        self.button_convert_date=QPushButton("Convertir plusieurs fichiers audio")
        self.button_convert_date.setFont(fontbig)
        self.button_convert_date.clicked.connect(self.convertdate_was_toggled)

        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        # status.setText(personne)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.button_add_user)
        self.layout.addWidget(self.button_remove_user)
        self.layout.addWidget(self.text_delete_files)
        self.layout.addWidget(self.button_delete_audio)
        self.layout.addWidget(self.button_delete_text)
        self.layout.addWidget(self.text_convert_audiofiles)
        self.layout.addWidget(self.button_convert)
        self.layout.addWidget(self.button_convert_date)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
        
    def add_was_clicked(self, s):
        print("Checked ?",s)
        
        dlg = Add_User()
         
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")
            
    def remove_was_clicked(self, s):
        print("Checked ?",s)
        
        dlg = Remove_User()
         
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
            print("User removed")
        else:
            print("Cancel!")
    def button_delete_audio_was_toggled(self, s):
        dlg = Delete_File(True)
         
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")
    
    def button_delete_text_was_toggled(self,s):
        dlg = Delete_File(False)
         
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")
            
    def convert_was_toggled(self):
        dlg = Convert_File()
         
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")
    
    def convertdate_was_toggled(self):
        dlg = Convert_Date()
        
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

                
    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)
        
# Add User dialog class definition
class Add_User(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter utilisateur")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.message_user = QLabel(self)
        self.message_user.setText("Nom d'utilisateur")
        self.message_user.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.message_user.setScaledContents(True)
        self.message_user.setFont(fontmedium)
        self.newuser=QLineEdit()
        
        message_user_prenom = QLabel("Prenom (optionnel)")
        message_user_prenom.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_user_prenom.setScaledContents(True)
        message_user_prenom.setFont(fontmedium)
        self.newuser_prenom=QLineEdit()
        message_user_nom = QLabel("Nom (optionnel)")
        message_user_nom.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_user_nom.setScaledContents(True)
        message_user_nom.setFont(fontmedium)
        self.newuser_nom=QLineEdit()
        
        self.layout.addWidget(self.message_user)
        self.layout.addWidget(self.newuser)
        self.layout.addWidget(message_user_prenom)
        self.layout.addWidget(self.newuser_prenom)
        self.layout.addWidget(message_user_nom)
        self.layout.addWidget(self.newuser_nom)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    def accept(self) -> None:
        if self.newuser.text() != "" :
            if not self.newuser_nom.text()  or not self.newuser_prenom.text() :
                fullname=""
            else :
                fullname=self.newuser_prenom.text()+" "+self.newuser_nom.text()
            db_manip.add_user(self.newuser.text(),fullname)
            return super().accept()
        else:
            pal = self.message_user.palette()
            pal.setColor(QPalette.WindowText, QColor("red"))
            self.message_user.setPalette(pal)
            self.message_user.setText("Nom d'utilisateur ne doit pas être vide")
    def reject(self) -> None:
        return super().reject()

# Remove User class dialog definition
class Remove_User(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enlever utilisateur")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.menu_user=QComboBox()
        self.menu_user.addItems(db_manip.get_users())
        self.menu_user.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menu_user.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menu_user.currentTextChanged.connect( self.text_changed )
        
        self.warningfiles=QLabel(self)
        pal = self.warningfiles.palette()
        if db_manip.get_audiodates(self.menu_user.currentText()) or db_manip.get_textdates(self.menu_user.currentText()) :
            pal.setColor(QPalette.WindowText, QColor("red"))
            warn_text="ATTENTION : Utilisateur avec enregistrements"
        else:
            pal.setColor(QPalette.WindowText, QColor("black"))
            warn_text="Utilisateur sans enregistrements"
        self.warningfiles.setPalette(pal)
        self.warningfiles.setScaledContents(True)
        self.warningfiles.setFont(fontsmall)
        self.warningfiles.setText(warn_text)
        
        self.layout.addWidget(self.menu_user)
        self.layout.addWidget(self.warningfiles)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def accept(self) -> None:
        if db_manip.get_audiodates(self.menu_user.currentText()) and db_manip.get_textdates(self.menu_user.currentText()) :
            dlg = Warning_files()
            dlg.setMinimumSize(QSize(400, 240))
            dlg.setMaximumSize(QSize(800, 480))
            if dlg.exec():
                print("Remove all files and user")
                return super().accept()
            else:
                print("Cancel!")
                return super().reject()
                
        elif db_manip.get_audiodates(self.menu_user.currentText()) :
            dlg = Warning_files()
            dlg.setMinimumSize(QSize(400, 240))
            dlg.setMaximumSize(QSize(800, 480))
            if dlg.exec():
                print("Remove audio files and user")
                return super().accept()
            else:
                print("Cancel!")
                return super().reject()

        elif db_manip.get_textdates(self.menu_user.currentText()) :
            dlg = Warning_files()
            dlg.setMinimumSize(QSize(400, 240))
            dlg.setMaximumSize(QSize(800, 480))
            if dlg.exec():
                print("Remove text files and user")
                return super().accept()
            else:
                print("Cancel!")
                return super().reject()
        else:
            print ("Remove User")
            db_manip.del_user(self.menu_user.currentText())
            return super().accept()
    
    def reject(self) -> None:
        return super().reject()

    
    def index_changed(self, i): # i is an int
        pal = self.warningfiles.palette()
        if db_manip.get_audiodates(self.menu_user.currentText()) or db_manip.get_textdates(self.menu_user.currentText()) :
            pal.setColor(QPalette.WindowText, QColor("red"))
            warn_text="ATTENTION : Utilisateur avec enregistrements"
        else:
            pal.setColor(QPalette.WindowText, QColor("black"))
            warn_text="Utilisateur sans enregistrements"
        self.warningfiles.setPalette(pal)
        self.warningfiles.setText(warn_text)
        print("index",i)
        
    def text_changed(self, s): # s is a str
        print(s)
        
# User with files Warning dialog class
class Warning_files(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ATTENTION !!!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.warning1=QLabel(self)
        pal = self.warning1.palette()
        pal.setColor(QPalette.WindowText, QColor("red"))
        self.warning1.setPalette(pal)
        self.warning1.setScaledContents(True)
        self.warning1.setFont(fontbig)
        self.warning1.setText("Utilisateur avec des fichiers")
        self.warning2=QLabel(self)
        pal = self.warning2.palette()
        pal.setColor(QPalette.WindowText, QColor("red"))
        self.warning2.setPalette(pal)
        self.warning2.setScaledContents(True)
        self.warning2.setFont(fontbig)
        self.warning2.setText("Tout effacer ?")
        
        self.layout.addWidget(self.warning1)
        self.layout.addWidget(self.warning2)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def accept(self) -> None:
        return super().accept()
    
    def reject(self) -> None:
        return super().reject()


# Delete (Audio or Text) File Dialog definition
class Delete_File(QDialog):
    def __init__(self, audio_flag):
        super().__init__()

        if audio_flag :
            wTitle="Effacer fichier Audio"
            mLabel="Fichiers Audio"
        else:
            wTitle="Effacer fichier Texte"
            mLabel="Fichiers Texte"
        
        self.setWindowTitle(wTitle)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(lambda: self.accept(audio_flag))
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.menu_user=QComboBox()
        self.menu_user.addItems(db_manip.get_users(True))
        self.menu_user.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menu_user.currentIndexChanged.connect(lambda: self.index_changed(audio_flag))
        # There is an alternate signal to send the text.
        self.menu_user.currentTextChanged.connect(self.text_changed)
        
        self.text_files=QLabel(mLabel)
        self.text_files.setScaledContents(True)
        self.text_files.setFont(fontmedium)
        
        if audio_flag :
            current_user=db_manip.get_audiodates(self.menu_user.currentText())
        else:
            current_user=db_manip.get_textdates(self.menu_user.currentText())
        
        # Menu déroulant fichiers audio
        self.menu_fichiers=QComboBox()
        f_items=[]
        for filen in current_user:
            f_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers.addItems(f_items)
        self.menu_fichiers.setFont(fontsmall)
        # Sends the current index (position) of the selected item.
        self.menu_fichiers.currentIndexChanged.connect( self.file_ind_changed )
        # There is an alternate signal to send the text.
        self.menu_fichiers.currentTextChanged.connect( self.file_changed )
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menu_user)
        self.layout.addWidget(self.text_files)
        self.layout.addWidget(self.menu_fichiers)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def accept(self,audio_flag) -> None:
        dlg = Warning_convert()
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        if dlg.exec():
            date_time_obj=datetime.datetime.strptime(self.menu_fichiers.currentText(),"%A %d %B %Y à %H:%M:%S")
            if audio_flag:
                fname=os.path.join(soundspath,self.menu_user.currentText(),db_manip.get_audiofile_name(self.menu_fichiers.currentText()))
                db_manip.del_audiofile([
                    fname,
                    date_time_obj.strftime("%Y%m%d"),
                    date_time_obj.strftime("%H%M%S"),
                    db_manip.get_audiofile_name(self.menu_fichiers.currentText()).replace(".mp3",""),
                    self.menu_user.currentText()])
            else:
                fname=os.path.join(textspath,self.menu_user.currentText(),db_manip.get_textfile_name(self.menu_fichiers.currentText()))
                db_manip.del_textfile([
                    fname,
                    date_time_obj.strftime("%Y%m%d"),
                    date_time_obj.strftime("%H%M%S"),
                    db_manip.get_textfile_name(self.menu_fichiers.currentText()).replace(".txt",""),
                    self.menu_user.currentText()])
            os.remove(fname)
            print("File deleted")
            return super().accept()
        else:
            print("Cancel!")
            return super().reject()
    
    def reject(self) -> None:
        return super().reject()

    def text_changed(self, s): # s is a str
        print(s)
        
    def index_changed(self, audio_flag): # i is an int
        self.menu_fichiers.clear()
        if audio_flag:
            current_user=db_manip.get_audiodates(self.menu_user.currentText())
        else:
            current_user=db_manip.get_textdates(self.menu_user.currentText())
        f_items=[]
        for filen in current_user:
            f_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers.addItems(f_items)
        
    def file_ind_changed(self, i): # i is an int
        print("index",i)

    def file_changed(self, s): # s is a str
        print(s)
        print(self.menu_fichiers.currentText())

# Convert Audio to Text Dialog definition
class Convert_File(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Convertir un fichier audio")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.menu_user=QComboBox()
        self.menu_user.addItems(db_manip.get_users())
        self.menu_user.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menu_user.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menu_user.currentTextChanged.connect( self.text_changed )
        
        self.text_audiofiles=QLabel("Fichiers Audio")
        self.text_audiofiles.setScaledContents(True)
        self.text_audiofiles.setFont(fontmedium)
        
        # Menu déroulant fichiers audio
        self.menu_fichiers_audio=QComboBox()
        current_user=db_manip.get_audiodates(self.menu_user.currentText())
        sound_items=[]
        for filen in current_user:
            sound_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers_audio.addItems(sound_items)
        self.menu_fichiers_audio.setFont(fontsmall)
        # Sends the current index (position) of the selected item.
        self.menu_fichiers_audio.currentIndexChanged.connect( self.file_ind_changed )
        # There is an alternate signal to send the text.
        self.menu_fichiers_audio.currentTextChanged.connect( self.file_changed )
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menu_user)
        self.layout.addWidget(self.text_audiofiles)
        self.layout.addWidget(self.menu_fichiers_audio)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def accept(self) -> None:
        dlg = Warning_convert()
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        if dlg.exec():
            sound_fname=os.path.join(soundspath,self.menu_user.currentText(),db_manip.get_audiofile_name(self.menu_fichiers_audio.currentText()))
            convert_audiofile(sound_fname,self.menu_user.currentText(),self.menu_fichiers_audio.currentText())
            print("File converted")
            return super().accept()
        else:
            print("Cancel!")
            return super().reject()
    
    def reject(self) -> None:
        return super().reject()

    def text_changed(self, s): # s is a str
        print(s)
        
    def index_changed(self, i): # i is an int
        self.menu_fichiers_audio.clear()
        print("index",i)
        current_user=db_manip.get_audiodates(self.menu_user.currentText())
        sound_items=[]
        for filen in current_user:
            sound_items.append(datetime.datetime(filen[0].year,filen[0].month,filen[0].day,
                                                 filen[1].hour,filen[1].minute,filen[1].second).strftime("%A %d %B %Y à %H:%M:%S"))
        self.menu_fichiers_audio.addItems(sound_items)
        
    def file_ind_changed(self, i): # i is an int
        print("index",i)

    def file_changed(self, s): # s is a str
        print(s)
        print(self.menu_fichiers_audio.currentText())

# Convert Audio to Text prior to a date Dialog
class Convert_Date(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Convertir plusieurs fichiers audios")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Date picker
        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QDateTime.currentDateTime())
        
        
        self.text=QLabel("Convertir les fichier antérieurs à :")
        self.text.setScaledContents(True)
        self.text.setFont(fontmedium)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.dateedit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def accept(self) -> None:
        dlg = Warning_convert()
        dlg.setMinimumSize(QSize(400, 240))
        dlg.setMaximumSize(QSize(800, 480))
        if dlg.exec():
            date_limit=self.dateedit.date().toPyDate().strftime("%Y%m%d")
            for audio_fname in db_manip.get_audiof_date(date_limit):
                usern=db_manip.get_users(audio_fname)
                sound_fname=os.path.join(soundspath,usern,audio_fname)
                fitem=datetime.datetime(int(audio_fname[:4]),int(audio_fname[4:6]),int(audio_fname[6:8]),
                                        int(audio_fname[9:11]),int(audio_fname[11:13]),int(audio_fname[13:15])).strftime("%A %d %B %Y à %H:%M:%S")
                convert_audiofile(sound_fname,usern,fitem)
            return super().accept()
        else:
            return super().reject()

    def reject(self) -> None:
        return super().reject()

# Convertion file Warning Dialog
class Warning_convert(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ATTENTION !!!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.warning1=QLabel(self)
        pal = self.warning1.palette()
        pal.setColor(QPalette.WindowText, QColor("red"))
        self.warning1.setPalette(pal)
        self.warning1.setScaledContents(True)
        self.warning1.setFont(fontbig)
        self.warning1.setText("Le(s) fichier(s) sera(ont) effacé(s)")
        self.warning2=QLabel(self)
        pal = self.warning2.palette()
        pal.setColor(QPalette.WindowText, QColor("red"))
        self.warning2.setPalette(pal)
        self.warning2.setScaledContents(True)
        self.warning2.setFont(fontbig)
        self.warning2.setText("Continuer ?")
        
        self.layout.addWidget(self.warning1)
        self.layout.addWidget(self.warning2)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def accept(self) -> None:
        return super().accept()
    
    def reject(self) -> None:
        return super().reject()

# Convert Audio to Text function
def convert_audiofile(fname,user,fitem):
    nfname=fname.replace("mp3","flac")
    data, samplerate = sf.read(fname)
    sf.write(nfname, data, samplerate)
    if check_internet_connection():
        print ("Online")
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(nfname) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data,language="fr-FR")
    else:
        print("Offline")
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(nfname)
        text=result["text"]
    if os.path.exists(nfname) :
        os.remove(nfname)
    if not os.path.exists(os.path.join(os.getcwd(),"texts")) :
        os.mkdir (os.path.join(os.getcwd(),"texts"))
    if not os.path.exists(os.path.join(os.getcwd(),"texts",user)):
        os.mkdir(os.path.join(os.getcwd(),"texts",user))
    tfname=fname.replace("sounds","texts")
    tfname=tfname.replace("mp3","txt")
    text_file = open(tfname, "w")
    text_file.write(text)
    text_file.close()
    date_time_obj=datetime.datetime.strptime(fitem,"%A %d %B %Y à %H:%M:%S")

    db_manip.add_textfile([
        os.path.join(textspath,user,db_manip.get_audiofile_name(fitem)).replace("mp3","txt"),
        date_time_obj.strftime("%Y%m%d"),
        date_time_obj.strftime("%H%M%S"),
        db_manip.get_audiofile_name(fitem).replace(".mp3",""),
        user
        ])
    
    db_manip.del_audiofile([
        os.path.join(soundspath,user,db_manip.get_audiofile_name(fitem)),
        date_time_obj.strftime("%Y%m%d"),
        date_time_obj.strftime("%H%M%S"),
        db_manip.get_audiofile_name(fitem).replace(".mp3",""),
        user])
    
    os.remove(fname)
    print("Converted....")