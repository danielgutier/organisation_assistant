import speech_recognition as sr

import whisper
import os

# Import the required module for text
# to speech conversion
# from gtts import gTTS

# This module is imported so that we can
# play the converted audio

import sounddevice as sd
import soundfile as sf

#import pyttsx3
import warnings
#warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
filename = "20230921_143423_Enseignant.mp3"
nfilename=filename.replace("mp3","flac")
data, samplerate = sf.read(filename)
sf.write(nfilename, data, samplerate)
print("Converting finished")

print(nfilename)

# Online solution
# initialize the recognizer
r = sr.Recognizer()

with sr.AudioFile(nfilename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data,language="fr-FR")
    print("Google : "+ text)

#offline solution
model = whisper.load_model("base")
result = model.transcribe(nfilename)
print("Whisper : "+ result["text"])

if os.path.exists(nfilename) :
    os.remove(nfilename)
"""
# The text that you want to convert to audio
with open ("D:/Users/braik/Documents/GymInf/Memoire/Git/organisation_assistant/texts/Père/20230927_172102_Père.txt",'r') as f:
    mytext = f.readlines()
f.close()
print (mytext[0])
# Language in which you want to convert
language = 'fr'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed

# Online solution 
myobj = gTTS(text=mytext[0], lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("welcome.mp3")

# Playing the converted file
data, fs = sf.read("welcome.mp3")
sd.play(data, fs)
sd.wait()


engine = pyttsx3.init()
voice = engine.getProperty('voices')[2] # the french voice
engine.setProperty('voice', voice.id)

engine.say(mytext[0]) # perfect

engine.runAndWait()
"""