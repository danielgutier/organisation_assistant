from PyQt5.QtWidgets import (
    QPushButton, QWidget, 
    QLabel, QVBoxLayout, QComboBox
    )
from PyQt5.QtCore import (
    Qt, QObject, 
    QThread, pyqtSignal
    )
from PyQt5.QtGui import QFont
import os, keyboard, sys, queue
import create_fname as create_fname
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from time import sleep
import db_manip


soundspath=os.path.join(os.getcwd(),"sounds")
# users=os.listdir(soundspath)
# for elem in users :
#     if not os.path.isdir(os.path.join(soundspath,elem)):
#         users.remove(elem)
        
q = queue.Queue()

fontbig=QFont('Helvetica',15)
fontmedium=QFont('Helvetica',12)
fontsmall=QFont('Helvetica',10)

global recording

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

class RecWorker(QObject):
    rec_finished=pyqtSignal()
    #rec_progress=pyqtSignal(int)
    def run (self,fname):
        recording=True
        #p=0
        print('recording : '+fname[0]+'.wav')
        with sf.SoundFile(fname[0]+'.wav', mode='x', samplerate=44100, channels=2, subtype='PCM_24') as file :
            with sd.InputStream(samplerate=44100, device=1, channels=2, callback=callback) :
                print('#' * 50)
                print('press Enter to stop the recording')
                print('#' * 50)
                while recording :
                    #p+=1
                    file.write(q.get())
                    #self.rec_progress.emit(p)
                    if keyboard.is_pressed("Enter"):
                        recording=False
                        print('\nRecording finished: ' + repr(fname[0]+'.wav'))
                        
        print("Converting file "+fname[0]+'.wav'+" ---> "+fname[0]+'.flac')
        sound = AudioSegment.from_file(fname[0]+'.wav', format="wav")
        sound.export(fname[0]+'.flac',format = "flac")
        if os.path.exists(fname[0]+'.flac') :
            os.remove(fname[0]+'.wav')
        print("Converting finished")
        
        self.rec_finished.emit()
        
        db_manip.add_audiofile(fname)
        
        
class Record(QWidget):
    def __init__(self):
        super().__init__()
        
        # Menu déroulant voix
        self.menuderoulant=QComboBox()
        
        self.menuderoulant.addItems(db_manip.get_users())
        self.menuderoulant.setFont(fontbig)
        # Sends the current index (position) of the selected item.
        self.menuderoulant.currentIndexChanged.connect( self.index_changed )
        # There is an alternate signal to send the text.
        self.menuderoulant.currentTextChanged.connect( self.text_changed )
        
        # Button REC
        self.button_rec=QPushButton("Enregistrer")
        self.button_rec.setFont(fontbig)
        self.button_rec.setEnabled(True)
        #self.button_rec.button_is_checked = False
        self.button_rec.clicked.connect(self.rec_was_toggled)
        
        # Button STOP
        self.button_stop=QPushButton("Arreter")
        self.button_stop.setFont(fontbig)
        self.button_stop.setEnabled(False)
        #self.button_stop.button_is_checked = False
        self.button_stop.clicked.connect(self.stop_was_toggled)
        
        # status line
        self.status = QLabel("Prêt")
        self.status.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.status.setScaledContents(True)
        self.status.setFont(fontsmall)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.menuderoulant)
        self.layout.addWidget(self.button_rec)
        self.layout.addWidget(self.button_stop)
        self.layout.addWidget(self.status)    

        self.setLayout(self.layout)        
    
        
    def rec_was_toggled(self):
        fname=create_fname.create_fname(soundspath,self.menuderoulant.currentText())
        #self.button_rec.setText("Arreter")
        self.status.setText("Enregistrement")
        self.thread=QThread()
        self.worker=RecWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda: self.worker.run(fname))
        self.worker.rec_finished.connect(self.thread.quit)
        self.worker.rec_finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.rec_progress.connect(self.reportProgress)
        self.thread.start()
        
        self.button_rec.setEnabled(False)
        self.button_stop.setEnabled(True)
        
        self.thread.finished.connect(
            lambda: self.button_rec.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.button_stop.setEnabled(False)
        )
        self.thread.finished.connect(
            lambda: self.status.setText("Prêt")
        )

    def stop_was_toggled(self):
        recording = False
        #self.status.setText("Enter appuyé")
        sleep(1)
        keyboard.press("Enter")
        #self.status.setText("Enregistrement")
        
        
    # def reportProgress(self, n):
    #     self.status.setText(f"Enregistrement: {n}")
                
    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)
