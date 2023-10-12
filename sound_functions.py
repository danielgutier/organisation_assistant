import sounddevice as sd
import soundfile as sf
import queue
import sys
import keyboard
from pydub import AudioSegment
import os
import datetime

q = queue.Queue()

def create_fname(path,source):
    path=str(path)
    source=str(source)
    if not os.path.exists(os.path.join(os.getcwd(),path)) :
        os.mkdir(os.path.join(os.getcwd(),path))
        
    if not os.path.exists(os.path.join(os.getcwd(),path,source)):
        os.mkdir(os.path.join(os.getcwd(),path,source))
    now=datetime.datetime.now()
    current_time=now.strftime("%H%M%S")
    # print(type(current_time))
    # print(current_time)

    current_date=now.strftime("%Y%m%d")
    # print(type(current_date))
    # print(current_date)

    # print(current_date+"_"+current_time+"_"+source)
    return(os.path.join(os.getcwd(),path,source,str(current_date+"_"+current_time+"_"+source)))
 
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def record_sound (sound_fname='sounds/test') :
    i=0
    file_exists=os.path.exists(sound_fname+'.wav')
    while file_exists :
        i+=1
        file_exists=os.path.exists(sound_fname+str(i)+'.wav')
    sound_fname=sound_fname+str(i)
    try :
        recording=True
        print('recording : '+sound_fname+'.wav')
        with sf.SoundFile(sound_fname+'.wav', mode='x', samplerate=44100, channels=2, subtype='PCM_24') as file :
            with sd.InputStream(samplerate=44100, device=1, channels=2, callback=callback) :
                print('#' * 50)
                print('press Enter to stop the recording')
                print('#' * 50)
                while recording :
                    file.write(q.get())
                    if keyboard.is_pressed("Enter"):
                        recording=False
                        print('\nRecording finished: ' + repr(sound_fname+'.wav'))
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(sound_fname+'.wav'))
    except Exception as e:
        print(e)
    print("Converting file "+sound_fname+'.wav'+" ---> "+sound_fname+'.flac')
    sound = AudioSegment.from_file(sound_fname+'.wav', format="wav")
    sound.export(sound_fname+'.flac',format = "flac")
    if os.path.exists(sound_fname+'.flac'
                      ) :
        os.remove(sound_fname+'.wav')
        print("Converting finished")
     
def play_sound (sound_fname='sounds/test0'):
    if os.path.exists(sound_fname+'.flac') :
        data, fs = sf.read(sound_fname+'.flac')
    elif os.path.exists(sound_fname+'.wav'):
        data, fs = sf.read(sound_fname+'.flac')
    sd.play(data, fs)
    sd.wait()

# record_sound(create_fname("sounds","enseignant"))
# play_sound(filename_with_path)