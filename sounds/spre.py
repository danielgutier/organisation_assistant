#import speech_recognition as sr

import whisper

import pyttsx3

filename = "Recording.wav"
#filename = "16-122828-0002.wav"
# initialize the recognizer
#r = sr.Recognizer()

# Online solution
"""with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data,language="fr-FR")
    print("Google : "+ text)
"""
#offline solution
model = whisper.load_model("base")
result = model.transcribe(filename)
print("Whisper : "+ result["text"])

# Import the required module for text
# to speech conversion
#from gtts import gTTS

# This module is imported so that we can
# play the converted audio

#import sounddevice as sd
#import soundfile as sf

# The text that you want to convert to audio
mytext = "Daniel dit, "+result["text"]

# Language in which you want to convert
#language = 'fr'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
# Online solution 
#myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
#myobj.save("welcome.mp3")

# Playing the converted file
#data, fs = sf.read("welcome.mp3")
#sd.play(data, fs)
#sd.wait()


engine = pyttsx3.init()
voice = engine.getProperty('voices')[2] # the french voice
engine.setProperty('voice', voice.id)

engine.say(mytext) # perfect

engine.runAndWait()