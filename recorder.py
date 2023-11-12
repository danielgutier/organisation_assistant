from PyQt5.QtWidgets import (
    QPushButton, QWidget, 
    QLabel, QVBoxLayout, QComboBox,
    QApplication
    )
from PyQt5.QtCore import (
    Qt
    )
from PyQt5.QtGui import QFont
import os, sys, queue
import datetime, locale
import sounddevice as sd
import soundfile as sf 
from pydub import AudioSegment
import db_manip
# Linux based system
locale.setlocale(locale.LC_TIME,'fr_CH.utf8')
# Windows based system
# locale.setlocale(locale.LC_TIME,'fr_FR')


soundspath=os.path.join(os.getcwd(),"sounds")
        
q = queue.Queue()

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy()) 
             
class Record(QWidget):
    def __init__(self):
        super().__init__()
        # Menu déroulant voix
        self.menuderoulant=QComboBox()
        users_items=db_manip.get_users()
        self.menuderoulant.addItems(users_items)
        self.menuderoulant.setFont(fontbig)
        
        # Button REC
        self.button_rec=QPushButton("Enregistrer")
        self.button_rec.setFont(fontbig)
        self.button_rec.setEnabled(True)
        self.button_rec.clicked.connect(self.rec_was_toggled)
        
        # Button STOP
        self.button_stop=QPushButton("Arreter")
        self.button_stop.setFont(fontbig)
        self.button_stop.setEnabled(False)
        self.button_stop.clicked.connect(self.stop_was_toggled)
        
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
        self.layout.addWidget(self.menuderoulant)
        self.layout.addWidget(self.button_rec)
        self.layout.addWidget(self.button_stop)
        self.layout.addStretch()
        self.layout.addWidget(self.button_refresh)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
    
        
    def rec_was_toggled(self):
        self.button_rec.setEnabled(False)
        self.button_stop.setEnabled(True)
        
        # Filename creation
        recuser=self.menuderoulant.currentText()
        if not os.path.exists(os.path.join(os.getcwd(),soundspath)) :
            os.mkdir(os.path.join(os.getcwd(),soundspath))
            
        if not os.path.exists(os.path.join(os.getcwd(),soundspath,recuser)):
            os.mkdir(os.path.join(os.getcwd(),soundspath,recuser))
        now=datetime.datetime.now()
        print(str(now))
        current_time=now.strftime("%H%M%S")
        current_date=now.strftime("%Y%m%d")
        fname=[os.path.join(os.getcwd(),soundspath,recuser,str(current_date+"_"+current_time+"_"+recuser)), current_date, current_time, str(current_date+"_"+current_time+"_"+recuser), recuser]

        # Change status bar text
        self.status.setText("Enregistrement")
        
        try:
            rec_flag=self.button_stop.isEnabled()
            print('recording : '+fname[0]+'.wav')
            with sf.SoundFile(fname[0]+'.wav', mode='x', samplerate=44100,
                          channels=1, subtype=None) as file :
                with sd.InputStream(samplerate=44100, device=None,
                                channels=1, callback=callback) :
                    print('#' * 60)
                    print('press ctrl+c to stop the recording')
                    print('#' * 60)
                    while rec_flag :
                        QApplication.processEvents()
                        file.write(q.get())
                        rec_flag=self.button_stop.isEnabled()
                        
        except KeyboardInterrupt:
            print ("Ctrl + c pressed")
        except Exception as e:
            print(e)               
        print('\nRecording finished: ' + repr(fname[0]+'.wav'))
        print("Converting file "+fname[0]+'.wav'+" ---> "+fname[0]+'.mp3')
        sound = AudioSegment.from_wav(fname[0]+'.wav')
        sound.export(fname[0]+'.mp3', format='mp3')
        if os.path.exists(fname[0]+'.mp3') :
            os.remove(fname[0]+'.wav')
        print("Converting finished")
        
        db_manip.add_audiofile(fname)

    def stop_was_toggled(self):
        print ("Arreter a été appuyé")
        self.button_rec.setEnabled(True)
        self.button_stop.setEnabled(False)
        self.status.setText("Prêt")
                
    def refresh_was_toggled(self): 
        self.menuderoulant.clear()
        users_items=db_manip.get_users()
        self.menuderoulant.addItems(users_items)
        